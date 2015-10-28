package org.cytoscape.ci;

/**
 * For Jackson Data binding
 * 
 *
 */
public class Result {
	
	// Unique Job ID
	public final String job_id;
	
	// ID of the worker
	public final String worker_id;
	
	// Result data location as URL string.
	public final String result;
	
	public Result(final String job_id, final String worker_id, final String result) {
		this.job_id = job_id;
		this.worker_id = worker_id;
		this.result = result;
	}

}
