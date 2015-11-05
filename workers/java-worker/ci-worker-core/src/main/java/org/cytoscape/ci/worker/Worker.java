package org.cytoscape.ci.worker;

public interface Worker {

	/**
	 * 
	 * Basic worker interface to perform actual 
	 * computation and return the result as serialized JSON
	 * 
	 * @param rawData input data as a serialized JSON string
	 * 
	 * @return result as a serialized JSON
	 * @throws Exception
	 */
	public String run(final String rawData) throws Exception;

	/**
	 * Start listening to messages via ZeroMQ
	 */
//	public void listen();
}
