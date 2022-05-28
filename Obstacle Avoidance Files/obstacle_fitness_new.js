{
    // here we define variables for record keeping
    fitnesses: [],

    setupSimulation: function() {
        // Reward cumulative travelling
        this.startPos = this.getRobot().getCoreComponent().getRootPosition();
        
        // calculate incremental step
        this.prevDistance = 0;
        
        // store cummulative distance
        this.cumDistance = 0;

        // previous max sensor and current max value
        this.prevMaxIr = 0;
        this.currMaxIr = 0;

        // Reward cumulative climbing
        this.prevAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        this.cumAltitude = 0;

        // obstacle avoid
        this.obstacle_avoid_reward = 0;

        // Penalize high number of motors
        this.motors = this.getRobot().getMotors();
        if (this.motors.length > 8 || this.motors.length == 0) {
            this.stopSimulationNow();
        }
        
        return true;
    },

    afterSimulationStep: function() {
        // Reward cumulative travelling
        var currPos = this.getRobot().getCoreComponent().getRootPosition();
        var currDistance = this.vectorDistance(currPos, this.startPos);
        var deltaDistance = currDistance - this.prevDistance;

        // cummulative distance
        this.cumDistance += deltaDistance;
        this.prevDistance = currDistance;

        // Reward cumulative climbing
        var currAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        var deltaAltitude = currAltitude - this.prevAltitude;
        this.cumAltitude += deltaAltitude;
        this.prevAltitude = currAltitude;

        // Maximum IR value accross sensors
		var sensors = this.getRobot().getSensors();
		var maxIr = 0
		for (var i = 0; i < sensors.length; i++) {
			if (/^Distance/.test(sensors[i].getLabel())) {
				if (sensors[i].read() > maxIr)
					maxIr = sensors[i].read();
			}
		}

		this.currMaxIr = maxIr;
        var deltaIR = this.currMaxIr - this.prevMaxIr;
        if (deltaDistance*deltaIR>0){
            this.obstacle_avoid_reward -= 1;
        }
        else{
            this.obstacle_avoid_reward += 1;
        }
        this.prevMaxIr = this.currMaxIr;
        return true;
    },

    endSimulation: function() {
        // Choose weighting factors for relative importance
        k_dist = 10;
		k_alt = 5;

        if (this.cumDistance>1){
            var fitness = this.cumDistance*(k_dist + k_alt*this.cumAltitude)*this.obstacle_avoid_reward;
        }
        else{
            var fitness = -10/(this.cumDistance+0.001);
        }

        console.log("cumdist: " + (this.cumDistance * k_dist) + " cumalt-wrt: " + (this.cumAltitude * k_alt*this.cumDistance) + " obstacle reward: " + (this.obstacle_avoid_reward));

        this.fitnesses.push(fitness);
		return true;
    },

    getFitness: function() {
        // Reject candidates with too many motors
        if (this.motors.length > 8 || this.motors.length == 0) {
            return -10000;
        }

        // Return the minimum fitness across evaluations
        fitness = this.fitnesses[0];
        for (var i = 1; i < this.fitnesses.length; i++) {
            if (this.fitnesses[i] < fitness)
                fitness = this.fitnesses[i];
        }
        return fitness;
    },

}
