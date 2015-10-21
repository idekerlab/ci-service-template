package org.cytoscape.ci;

public class ServiceParameter {
	
	public final String name;
	public final String type;
	public final String description;
	public final Boolean required;


	public ServiceParameter(final String name, final String type, final String description, final Boolean required) {
		this.name = name;
		this.type = type;
		this.description = description;
		this.required = required;
	}
}
