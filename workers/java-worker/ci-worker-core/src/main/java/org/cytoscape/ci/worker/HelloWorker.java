package org.cytoscape.ci.worker;

import java.util.HashMap;
import java.util.Map;

import org.cytoscape.ci.BaseWorker;

/**
 * Sample Worker 1: HelloWorker
 * 
 *  - Simply pass through given message from the service.
 *
 */
public class HelloWorker extends BaseWorker {

	@Override
	public String run(final String rawData) throws Exception {
		@SuppressWarnings("unchecked")
		final Map<String, String> dataMap = mapper.readValue(rawData, Map.class);

		final Map<String, String> result = new HashMap<>();
		result.put("reply", "Your message is: " + dataMap.get("message"));

		// Sleep to emulate long running task...
		Thread.sleep(5000);
		
		// Return message as a serialized JSON
		return mapper.writeValueAsString(result);
	}
}