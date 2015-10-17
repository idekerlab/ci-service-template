package org.cytoscape.ci;

public class JobStatus { 

	public final String job_id;
	public final String worker_id;
	public final String status;

	public JobStatus(final String job_id, final String worker_id, final String status) {
		this.job_id = job_id;
		this.worker_id = worker_id;
		this.status = status;
	}
}
