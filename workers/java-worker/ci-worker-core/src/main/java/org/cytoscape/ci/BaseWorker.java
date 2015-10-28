package org.cytoscape.ci;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import org.zeromq.ZMQ;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import redis.clients.jedis.Jedis;

public class BaseWorker implements Worker {

	private static final Logger logger = Logger.getLogger("worker");

	private static final String REDIS_TAG_ENDPOINTS = "endpoints";
	private static final String REDIS_TAG_DESCRIPTION = "description";
	private static final String REDIS_TAG_PARAMETERS = "parameters";

	private ZMQ.Context context;
	private ZMQ.Socket queue;
	private ZMQ.Socket collector;
	private ZMQ.Socket monitor;

	final String id;

	// The following will be set by Jackson Data Mapper
	public String endpoint;
	public String description;
	public Integer instances;

	String resultServerLocation;
	String dataServerLocation;

	public Collection<ServiceParameter> parameters;

	private final ObjectMapper mapper;

	public BaseWorker() {
		this.id = IdGenerator.getID().toString();
		this.mapper = new ObjectMapper();
	}

	protected final void initZmqConnections(final String redisIp, final Integer redisPort, final String taskQueueIp,
			final Integer taskQueuePort, final String collectorIp, final Integer collectorPort, final String monitorIp,
			final Integer monitorPort) throws JsonProcessingException {

		// Setup Redis Client
		final Jedis redisClient = new Jedis(redisIp, redisPort);
		final Map<String, String> registeredEndpoints = redisClient.hgetAll(REDIS_TAG_ENDPOINTS);

		logger.info("!Registered endpoints: " + registeredEndpoints.keySet());

		if (registeredEndpoints.keySet().contains(this.endpoint) == false) {
			logger.info("## Registering service: " + endpoint + ", Port " + taskQueuePort);

			redisClient.hset(REDIS_TAG_ENDPOINTS, this.endpoint, taskQueuePort.toString());
			redisClient.hset(this.endpoint, REDIS_TAG_DESCRIPTION, this.description);

			final String serializedParams = mapper.writeValueAsString(parameters);
			logger.info("Serialized params: " + serializedParams);

			redisClient.hset(endpoint, REDIS_TAG_PARAMETERS, serializedParams);

			logger.info("Service registered: " + endpoint + ", Port " + taskQueuePort);
		} else {
			logger.info("No need to register: " + this.endpoint);
		}
		redisClient.close();

		// ZeroMQ settings

		this.context = ZMQ.context(1);

		// Socket to connect to task queue
		this.queue = context.socket(ZMQ.PULL);
		String queueUrlString = "tcp://" + taskQueueIp + ":" + taskQueuePort.toString();
		this.queue.connect(queueUrlString);

		logger.info("Queue: " + queueUrlString);

		// Socket to push result to collector
		this.collector = context.socket(ZMQ.PUSH);
		this.collector.connect("tcp://" + collectorIp + ":" + collectorPort.toString());

		// Socket to send messages to monitor
		this.monitor = context.socket(ZMQ.PUSH);
		this.monitor.connect("tcp://" + monitorIp + ":" + monitorPort.toString());
	}

	public void listen() {

		while (!Thread.currentThread().isInterrupted()) {
			logger.info("Worker ID: " + this.id + " is listening...");

			// Get input data as raw String
			byte[] val = queue.recv(0);
			logger.info("Got Data byte: " + val);

			final String dataString = new String(val);
			logger.info("Got Data: " + dataString);

			// Use Jackson Object Mapper to create pojo from JSON string
			InputData inputData;
			try {
				inputData = mapper.readValue(dataString, InputData.class);
				// Create status message JSON
				final JobStatus status = new JobStatus(inputData.job_id, id, "running");
				monitor.send(mapper.writeValueAsString(status));

				logger.info("Data location => " + inputData.data);
				URL inputDataLocationUrl = new URL(inputData.data);
				final String inputDataString = mapper.readValue(inputDataLocationUrl, String.class);

				logger.info("Got Input Data => " + inputDataString);
				final String result = run(inputDataString);
				logger.info("Result => " + result);

				final String resultFileId = postResultToServer(result);
				final String resultFileURL = resultServerLocation + "data/" + resultFileId;
				// TODO: send result to file server
				final Result resultObj = new Result(inputData.job_id, id, resultFileURL);
				final String resultAsString = mapper.writeValueAsString(resultObj);

				logger.info("------- Sending result to collector => " + resultAsString);

				collector.send(resultAsString);

			} catch (Exception e) {
				e.printStackTrace();
				throw new RuntimeException("Could not process job.", e);
			} finally {
				collector.close();
				queue.close();
				context.term();
			}
		}
	}

	private final String postResultToServer(final String data) throws IOException {

		logger.info("POSTing result to result file server => " + data);

		// URL for the Data cache server
		final URL url = new URL(resultServerLocation + "data");

		final HttpURLConnection connection = (HttpURLConnection) url.openConnection();
		connection.setDoOutput(true);
		connection.setDoInput(true);
		connection.setRequestMethod("POST");
		connection.setRequestProperty("Content-Type", "application/json");
		connection.setRequestProperty("Accept", "application/json");

		final BufferedWriter writer = new BufferedWriter(
				new OutputStreamWriter(connection.getOutputStream(), StandardCharsets.UTF_8));
		writer.write(data);
		writer.flush();

		StringBuilder sb = new StringBuilder();
		int HttpResult = connection.getResponseCode();
		if (HttpResult == HttpURLConnection.HTTP_OK) {
			BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"));
			String line = null;
			while ((line = br.readLine()) != null) {
				sb.append(line + "\n");
			}

			br.close();
			Map<String, String> resultMap = mapper.readValue(sb.toString(), Map.class);
			return resultMap.get("fileId");
		} else {
			System.out.println("ERROR!");
			throw new IOException("Could not POST result to file server: " + connection.getResponseMessage());
		}
	}

	@Override
	public String run(final String rawData) throws Exception {
		Map dataMap = mapper.readValue(rawData, Map.class);

		dataMap.keySet().stream().forEach(key -> logger.info(key.toString() + ": " + dataMap.get(key).toString()));

		final Map<String, String> result = new HashMap<>();
		result.put("response_message", "OK");

		return mapper.writeValueAsString(result);
	}
}