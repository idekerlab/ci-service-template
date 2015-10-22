package org.cytoscape.ci;

import java.net.URL;
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
	
	public Collection<ServiceParameter> parameters;
	
	private final ObjectMapper mapper;
	
	public BaseWorker() {
		this.id = IdGenerator.getID().toString();
		this.mapper = new ObjectMapper();
	}

	protected final void initZmqConnections(
			final String redisIp, final Integer redisPort,
			final String taskQueueIp, final Integer taskQueuePort,
			final String collectorIp, final Integer collectorPort,
			final String monitorIp, final Integer monitorPort) throws JsonProcessingException {
		
		// Setup Redis Client
		final Jedis redisClient = new Jedis(redisIp, redisPort);
		final Map<String, String> registeredEndpoints = redisClient.hgetAll(REDIS_TAG_ENDPOINTS);
		
		logger.info("!Registered endpoints: " + registeredEndpoints.keySet());
		
		if(registeredEndpoints.keySet().contains(this.endpoint) == false) {
			logger.info("## Registering service: " + endpoint + ", Port " + taskQueuePort);
			
			redisClient.hset(REDIS_TAG_ENDPOINTS, this.endpoint, taskQueuePort.toString());
			redisClient.hset(this.endpoint, REDIS_TAG_DESCRIPTION, this.description);
			
			final String serializedParams = mapper.writeValueAsString(parameters);
			logger.info("$$$$$$$$$$$$$$$$$$$$$$Serialized params: " + serializedParams);
			
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

		while (true) {
//		while (!Thread.currentThread().isInterrupted()) {
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
				
				// TODO: send result to file server
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}

		//collector.close();
		//queue.close();
		//context.term();
	}
	
	@Override
	public String run(final String rawData) throws Exception {
		Map dataMap = mapper.readValue(rawData, Map.class);
		
		dataMap.keySet().stream()
			.forEach(key->logger.info(key.toString() + ": " + dataMap.get(key).toString()));
		
		final Map<String, String> result= new HashMap<>();
		result.put("result", "OK");
		
		return mapper.writeValueAsString(result);
	}
}