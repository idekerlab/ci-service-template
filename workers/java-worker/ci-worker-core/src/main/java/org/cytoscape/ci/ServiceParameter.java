package org.cytoscape.ci;

public class ServiceParameter {
	
	private final String name;
	private final Class<?> type;
	private final String description;


	public ServiceParameter(final String name, final Class<?> type, final String description) {
		this.name = name;
		this.type = type;
		this.description = description;
	}


	public String getName() {
		return name;
	}


	public Class<?> getType() {
		return type;
	}


	public String getDescription() {
		return description;
	}

}
