package org.cytoscape.ci;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Collection;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.zeromq.ZMQ;

import redis.clients.jedis.Jedis;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Worker {

	private final Logger logger = Logger.getLogger("worker");
	
	private static final String REDIS_ENDPOINTS = "endpoints";
	private static final String REDIS_DESCRIPTION = "description";

	private ZMQ.Context context;
	private ZMQ.Socket queue;
	private ZMQ.Socket collector;
	private ZMQ.Socket monitor;

	// Redis Client for Java
	private Jedis redisClient;

	// Url of the server
	private final URL resultFileServer;

	private final String endpoint;
	private final String description;
	private final String id;
	private final Collection<ServiceParameter> parameters;

	/**
	 * Base Java Worker class
	 * 
	 * @param endpoint Endpoint of the service.
	 * @param description Description of the service
	 * @param parameters
	 * @param id Worker ID
	 * @param resultFileServerUrl
	 * @param redisServerIp
	 * @param redisServerPort
	 * @param serverIP
	 * @param recieverPort
	 * @param senderPort
	 * @param monitorPort
	 */
	public Worker(
			final String endpoint,
			final String description,

			final Collection<ServiceParameter> parameters,

			final String id,

			final String resultFileServerUrl,

			final String redisServerIp,
			final Integer redisServerPort,

			final String serverIP,
			final Integer recieverPort,
			final Integer senderPort,
			final Integer monitorPort
		) {

		logger.setLevel(Level.INFO);
		
		// Set basic parameters

		if (endpoint == null || endpoint.isEmpty()) {
			throw new IllegalArgumentException(
					"Endpoint parameter should ne non-empty string.");
		} else {
			this.endpoint = endpoint;
		}

		this.id = id;
		this.description = description;
		this.parameters = parameters;

		// Setup server URLs
		try {
			this.resultFileServer = new URL(resultFileServerUrl);
		} catch (MalformedURLException e) {
			throw new IllegalArgumentException(
					"Invalid URL for the result file server.");
		}

		// Create Redis Client
		this.redisClient = new Jedis(redisServerIp, redisServerPort);

		this.initZmqConnections(serverIP, monitorPort, serverIP, monitorPort,
				serverIP, monitorPort);
	}

	private final void initZmqConnections(
			final String taskQueueIp, final Integer taskQueuePort,
			final String collectorIp, final Integer collectorPort,
			final String monitorIp, final Integer monitorPort) {
		
		final Map<String, String> registeredEndpoints = this.redisClient.hgetAll(REDIS_ENDPOINTS);
		
		if(registeredEndpoints.keySet().contains(this.endpoint)) {
			redisClient.hset(REDIS_ENDPOINTS, this.endpoint, taskQueuePort.toString());
			redisClient.hset(this.endpoint, REDIS_DESCRIPTION, this.description);
			
			// TODO Serialze parameter object into JSON using Jackson Databind.
			//serializedParams = json.dumps(parameters);
			//self.redis_conn.hset(endpoint, "parameters", serialized_params)

			logger.info("Service registered: " + endpoint + ", Port " + taskQueuePort);
		} else {
			logger.info("No need to register: " + this.endpoint);
		}
		
		// ZeroMQ settings
		
		this.context = ZMQ.context(1);

		// Socket to connect to task queue
		this.queue = context.socket(ZMQ.PULL);
		this.queue.connect("tcp://" + taskQueueIp + ":" + taskQueuePort.toString());

		// Socket to push result to collector
		this.collector = context.socket(ZMQ.PUSH);
		this.collector.connect("tcp://" + collectorIp + ":" + collectorPort.toString());

		// Socket to send messages to monitor
		this.monitor = context.socket(ZMQ.PUSH);
		this.monitor.connect("tcp://" + monitorIp + ":" + monitorPort.toString());
		
	}

	public void listen() throws IOException {
		System.out.println("Java Worker: listening...");

		while (!Thread.currentThread().isInterrupted()) {
			// Get input data as raw String
			final String dataString = new String(queue.recv(0)).trim();

			// Use Jackson Object Mapper to create pojo from JSON string
			final ObjectMapper mapper = new ObjectMapper();
			final InputData inputData = mapper.readValue(dataString, InputData.class);
			
			// Create status message JSON
			final JobStatus status = new JobStatus(inputData.job_id, id, "running");
			monitor.send(mapper.writeValueAsString(status));
			
			logger.info("Data location => " + inputData.data);

		}

		collector.close();
		queue.close();
		context.term();
	}

	public static void main(String[] args) {
		
		// Parse command-line options and 
		CommandLineParser parser = new DefaultParser();
		Options options = new Options();
		
		options.addOption("e", "endpoint", true, "Endpoint");
		options.addOption("d", "description", true, "Description of the service");
		options.addOption("i", "id", true, "Unique ID of the worker");
		
		options.addOption("s", "result-server", true, "Result file server IP Address");
		options.addOption("r", "redis", true, "Redis IP address");

		options.addOption("q", "queue-port", true, "Task queue port number");
		options.addOption("c", "collector-port", true, "Collector port number");
		options.addOption("m", "monitor-port", true, "Monitor port number");

		Worker worker = null;

		try {
			// parse the command line arguments
			CommandLine line = parser.parse(options, args);

			String serverIpAddress = "localhost";

			if (line.hasOption("s")) {
				serverIpAddress = line.getOptionValue("s");
			}
			final String endpoint = line.getOptionValue("e");
			final String description = line.getOptionValue("d");
			final String id = line.getOptionValue("i");
			
			final String queuePort = line.getOptionValue("q");
			final String collectorPort = line.getOptionValue("c");
			final String monitorPort = line.getOptionValue("m");

			worker = new Worker(
					endpoint,
					description,
					null,
					id,
					
					resultFileServerUrl,

					redisServerIp,
					InredisServerPort,

	
					Integer.parseInt(queuePort),
					Integer.parseInt(collectorPort),
					Integer.parseInt(monitorPort));

			worker.listen();

		} catch (Exception exp) {
			exp.printStackTrace();
			System.out.println("Unexpected exception:" + exp.getMessage());
		}
	}
}
