package org.cytoscape.ci.worker.nbs;

import org.cytoscape.ci.worker.BaseWorker;

public class NBSWorker extends BaseWorker {

	@Override
	public String run(final String rawData) throws Exception {
		
		System.out.println("NBS worker called!");
		
		// Jackson parse the JSON string and creates Java object
		final NBSInput parsedParameters = mapper.readValue(rawData, NBSInput.class);
		
		// Extract parameters, etc.
		final String inputFile = parsedParameters.inputFile;
		System.out.println(inputFile);
		
		// Here, you can call existing NBS worker code...
		
		
		// Somehow you need to create new result object.
		final NBSResult result = new NBSResult();
		result.result = "Dummy result";
		
		
		Thread.sleep(5000);
		
		// This returns serialized JSON of your result
		String serializedResult = mapper.writeValueAsString(result);
		
		System.out.println(serializedResult);
		
		return serializedResult;
	}

}
