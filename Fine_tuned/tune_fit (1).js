{
	// here we define a variable for record keeping
	
	fitnesses : [],

	// function called at the beginning of each simulation
	
	setupSimulation: function() {
		this.startPos = this.getRobot().getCoreComponent().getRootPosition();
		this.totalAltitude = 0.0;
		this.currentAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
		this.fitnesses = [];
		return true;
	},
	
	afterSimulationStep: function() {
		  this.totalAltitude = this.totalAltitude + (this.getRobot().getCoreComponent().getRootPosition().z - this.currentAltitude);
		  this.currentAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
		  console.log("sim step: "+this.totalAltitude);
		  return true;
	},

	// function called at the end of each simulation
	endSimulation: function() {
	
		var coreComponentDistance = this.getRobot().getCoreComponent().getRootPosition();
		var distance = this.vectorDistance(coreComponentDistance, this.startPos);
		var total_altitude = this.totalAltitude;
		console.log("fitness: "+distance+"_"+total_altitude);
		
		if (distance<0.3){
			this.fitnesses.push(0);
			return true;
		}
		
		var fitness =distance*(1 + 100*total_altitude);
		
		this.fitnesses.push(fitness);
		return true;
	},

	// function to get fitness
	getFitness: function() {
		var worse_fitness = this.fitnesses[0];
		for (var i = 0; i < this.fitnesses.length; i++) {
		     if (this.fitnesses[i] < worse_fitness) {
			 worse_fitness = this.fitnesses[i];
			}
		 }
		
		return worse_fitness;
	},
}
