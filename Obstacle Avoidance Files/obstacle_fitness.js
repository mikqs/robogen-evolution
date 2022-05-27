{
    // here we define variables for record keeping
    fitnesses: [],

    setupSimulation: function() {
        // Reward cumulative travelling
        this.startPos = this.getRobot().getCoreComponent().getRootPosition();
        this.prevDistance = 0;
        this.cumDistance = 0;

        // Reward cumulative climbing
        this.prevAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        this.cumAltitude = 0;

        // For obstacle avoidance
        this.maxIrVals = [];
        this.cumMaxIrVals = 0;

        //TODO: look at motor torques/velocities with distance

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
        if (deltaDistance > 0) {
            this.cumDistance += deltaDistance;
        }
        else {
            this.cumDistance -= deltaDistance;
        }
        this.prevDistance = currDistance;

        // Reward cumulative climbing
        var currAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        var deltaAltitude = currAltitude - this.prevAltitude;
        if (deltaAltitude > 0) {
            this.cumAltitude += deltaAltitude;
        }
        this.prevAltitude = currAltitude;

        // Stability
        // var roll = Math.abs(this.getRobot().getCoreComponent().getRootAttitude().x);
        // var pitch = Math.abs(this.getRobot().getCoreComponent().getRootAttitude().y);
        // this.cumUnstab += roll + pitch;

        // Maximum IR value accross sensors
		var sensors = this.getRobot().getSensors();
		var maxIr = 0
		for (var i = 0; i < sensors.length; i++) {
			if (/^Distance/.test(sensors[i].getLabel())) {
				if (sensors[i].read() > maxIr)
					maxIr = sensors[i].read();
			}
		}
		this.maxIrVals.push(maxIr);
		this.cumMaxIrVals += maxIr;

        return true;
    },

    endSimulation: function() {
		// Reward all body parts ending up far from start position
		var minPartDist = Number.MAX_VALUE;
		bodyParts = this.getRobot().getBodyParts();
		for (var i = 0; i < bodyParts.length; i++) {
			var partDist = this.vectorDistance(bodyParts[i].getRootPosition(), this.startPos);
            if (partDist < minPartDist)
			    minPartDist = partDist;
		}

        // Choose weighting factors for relative importance
        k_dist = 10;
		k_alt = 5;
		k_distend = 100;
		k_ir = 0.1;

		if (this.cumMaxIrVals < 0.1){
		    console.log("no interaction with obstacles");
		    this.fitnesses.push(-10000)
        } else {
            console.log("cumdist: " + (this.cumDistance * k_dist) + " cumalt: " + (this.cumAltitude * k_alt) + " distendminpart: " + (minPartDist * k_distend) + " cumMaxIR: " + (-this.cumMaxIrVals * k_ir));
            var fitness = (this.cumDistance * k_dist) + (this.cumAltitude * k_alt) + (minPartDist * k_distend) - (this.cumMaxIrVals * k_ir);
            this.fitnesses.push(fitness);

        }
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
