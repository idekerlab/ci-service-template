package org.cytoscape.ci;

import java.util.LinkedHashMap;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;

public class WorkerBuilder {
	
	// Basic worker information
	private static final String ENDPOINT = "endpoint";
	private static final String DESCRIPTION = "description";
	
	// Server Section
	private static final String SERVERS = "servers";
	
	private static final String TASK_QUEUE = "task_queue";
	private static final String COLLECTOR = "collector";
	private static final String MONITOR = "monitor";
	private static final String REDIS = "redis";
	private static final String RESULT= "result";
	private static final String DATA_CACHE = "datacache";
	
	private static final String LOCATION = "location";
	private static final String PORT = "port";
	
	// Parameters
	private static final String PARAMETERS = "parameters";
	private static final String NAME = "name";
	private static final String TYPE = "type";
	private static final String REQUIRED = "required";
	
	// Default Values
	private static final Integer DEFAULT_REDIS_PORT = 6379;
	

	public Worker build(final LinkedHashMap<String, ?> params) throws JsonProcessingException {
	
		// Create an empty instance
		final Worker worker = new Worker();
		
		// Set all required parameters
		Object endpoint = params.get(ENDPOINT);
		if(endpoint == null || endpoint.toString().isEmpty()) {
			throw new IllegalArgumentException("Endpoint should be non-empty text.");
		}
		worker.endpoint = endpoint.toString();
		
		Object description = params.get(DESCRIPTION);
		if(description != null && description.toString().isEmpty() == false) {
			worker.description = description.toString();
		} else {
			worker.description = "";
		}
		
		Object servers = params.get(SERVERS);
		if(servers == null) {
			throw new NullPointerException("Servers parameter is required.");
		}

		setServers(worker, (Map<String, ?>) servers);
		return worker; 
	}
	
	private final void setServers(final Worker worker, final Map<String, ?> serverParams) throws JsonProcessingException {
		
		final Map<String ,?> taskQueue = (Map<String, ?>) serverParams.get(TASK_QUEUE);
		final String taskQueueIp = taskQueue.get(LOCATION).toString();
		final Integer taskQueuePort = Integer.parseInt(taskQueue.get(PORT).toString());

		final Map<String, ?> collector = (Map<String, ?>) serverParams.get(COLLECTOR);
		final String collectorIp = collector.get(LOCATION).toString();
		final Integer collectorPort = Integer.parseInt(collector.get(PORT).toString());
		
		final Map<String, ?> monitor = (Map<String, ?>) serverParams.get(MONITOR);
		final String monitorIp = monitor.get(LOCATION).toString();
		final Integer monitorPort = Integer.parseInt(monitor.get(PORT).toString());
		
		final Map<String, ?> redis = (Map<String, ?>) serverParams.get(REDIS);
		final String redisIp = redis.get(LOCATION).toString();
		final Integer redisPort = Integer.parseInt(redis.get(PORT).toString());
		
		worker.initZmqConnections(
				redisIp, redisPort,
				taskQueueIp, taskQueuePort,
				collectorIp, collectorPort,
				monitorIp, monitorPort);
		
		// Data cache and result file servers
		final Map<String, ?> result = (Map<String, ?>) serverParams.get(RESULT);
		final Map<String, ?> dataCache = (Map<String, ?>) serverParams.get(DATA_CACHE);
		
	}
	
	private final void setServerDetails(final Worker worker, Map<String, ?> details) {
		
	}

}
