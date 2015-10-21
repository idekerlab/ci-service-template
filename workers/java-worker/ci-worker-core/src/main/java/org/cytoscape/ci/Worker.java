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

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Worker {

	private static final Logger logger = Logger.getLogger("worker");
	
	private static final String REDIS_TAG_ENDPOINTS = "endpoints";
	private static final String REDIS_TAG_DESCRIPTION = "description";
	private static final String REDIS_TAG_PARAMETERS = "parameters";
	
	private ZMQ.Context context;
	private ZMQ.Socket queue;
	private ZMQ.Socket collector;
	private ZMQ.Socket monitor;

	private String id;

	// The following will be set by Jackson Data Mapper
	public String endpoint;
	public String description;
	public Integer instances;
	
	public ServiceParameter parameters;
	

	protected final void initZmqConnections(
			final String redisIp, final Integer redisPort,
			final String taskQueueIp, final Integer taskQueuePort,
			final String collectorIp, final Integer collectorPort,
			final String monitorIp, final Integer monitorPort) throws JsonProcessingException {
		
		// Setup Redis Client
		final Jedis redisClient = new Jedis(redisIp, redisPort);
		final Map<String, String> registeredEndpoints = redisClient.hgetAll(REDIS_TAG_ENDPOINTS);
		
		if(registeredEndpoints.keySet().contains(this.endpoint)) {
			
			redisClient.hset(REDIS_TAG_ENDPOINTS, this.endpoint, taskQueuePort.toString());
			redisClient.hset(this.endpoint, REDIS_TAG_DESCRIPTION, this.description);
			
			final ObjectMapper mapper = new ObjectMapper();
			
			final String serializedParams = mapper.writeValueAsString(parameters);
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
	
	public void run() throws Exception {
		
	}
}