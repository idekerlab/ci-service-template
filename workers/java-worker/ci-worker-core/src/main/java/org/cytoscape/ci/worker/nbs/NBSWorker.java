package org.cytoscape.ci.worker.nbs;

import org.cytoscape.ci.BaseWorker;

public class NBSWorker extends BaseWorker {

	@Override
	public String run(final String rawData) throws Exception {
		
		// Jackson parse the JSON string and creates Java object
		final NBSInput parsedParameters = mapper.readValue(rawData, NBSInput.class);
		
		
		// Here, you can call existing NBS worker code...
		
		
		// Somehow you need to create new result object.
		final NBSResult result = new NBSResult();
		
		// This returns serialized JSON of your result
		return mapper.writeValueAsString(result);
	}

}
