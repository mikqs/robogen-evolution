{

	// variable 1 for z 
	// variable 2 for roll, pitch
	maxAccVals1 : [],
	maxAccVals2 : [],
	fitnesses: [],
	
		setupSimulation: function() {
				// record the starting position
				this.startPos = this.getRobot().getCoreComponent().getRootPosition();
				this.maxAccVals1 = [];
				this.maxAccVals2 = [];
				this.fitnesses = [];
				return true;
		},
	
	// optional function called after each step of simulation
		afterSimulationStep: function() {
		
			sensors = this.getRobot().getCoreComponent().getSensors();
			
			for (var i = 0; i < sensors.length; i++) {
				sensor = sensors[i];
				
				if (sensor.getType()=="ImuSensorElement") {
					var label = sensor.getLabel();
					var sensorVal = Math.abs((sensor.read())/25);
					
					if (/z-acceleration$/.test(label)) {
							this.maxAccVals1.push(sensorVal);
					}
					
					 if(/Roll$/.test(label)) {
							 this.maxAccVals2.push(sensorVal*2);
					 }
					 
					 if(/Pitch$/.test(label)) {
							this.maxAccVals2.push(sensorVal*2);
					 }
				}
			}
			return true;
		},
		
		endSimulation: function() {
				// find the distance between the starting position and ending position
				var currentPos = this.getRobot().getCoreComponent().getRootPosition();
				var xDiff = (currentPos.x - this.startPos.x);
				var yDiff = (currentPos.y - this.startPos.y);
				var fitness = Math.sqrt(Math.pow(xDiff,2) + Math.pow(yDiff,2))*4;
				
				var maxReading1 = Number.MIN_VALUE;
		
				for (var i = 0; i < this.maxAccVals1.length; i++) {
					reading1 = this.maxAccVals1[i];
					if (reading1 > maxReading1) {
						maxReading1 = reading1;
					 }
				  }
		
				  var maxReading2 = Number.MIN_VALUE;
		
				  for (var i = 0; i < this.maxAccVals2.length; i++) {
					  reading2 = this.maxAccVals2[i];
					  if (reading2 > maxReading2) {
						maxReading2 = reading2;
					   }
				  }
		
				  fitness -= (maxReading1 +  maxReading2);
				  this.fitnesses.push(fitness);	
				  return true;
		},
	
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
