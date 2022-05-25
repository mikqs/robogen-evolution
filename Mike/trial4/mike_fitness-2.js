{
    // here we define variables for record keeping
    fitnesses: [],

    setupSimulation: function() {
        // Reward cumulative travelling
        this.dist_progress_counter = 0;
        this.startPos = this.getRobot().getCoreComponent().getRootPosition();
        this.prevDistance = 0;
        this.cumDistance = 0;

        // Reward cumulative climbing
        this.alt_progress_counter = 0;
        this.prevAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        this.cumAltitude = 0;

        // Penalize high number of motors
        this.motors = this.getRobot().getMotors();
        if (this.motors.length > 8 || this.motors.length == 0) {
            this.stopSimulationNow();
        }

        //TODO: look at motor torques/velocities with distance

        return true;
    },

    afterSimulationStep: function() {
        // Reward cumulative travelling
        var currPos = this.getRobot().getCoreComponent().getRootPosition();
        var currDistance = this.vectorDistance(currPos, this.startPos);
        var deltaDistance = currDistance - this.prevDistance;
        if (deltaDistance > 0.02) {
            this.dist_progress_counter += 1;
            this.cumDistance += (deltaDistance) * this.dist_progress_counter;
        } else {
            this.dist_progress_counter = 0;
			this.cumDistance += (deltaDistance)*2;
        }
        this.prevDistance = currDistance;

        // Reward cumulative climbing
        var currAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        var deltaAltitude = currAltitude - this.prevAltitude;
        if (deltaAltitude > 0.002) {
            this.alt_progress_counter += 1;
            this.cumAltitude += (deltaAltitude) * this.alt_progress_counter;
        } else {
            this.alt_progress_counter = 0;
        }
        this.prevAltitude = currAltitude;

        // var roll = Math.abs(this.getRobot().getCoreComponent().getRootAttitude().x);
        // var pitch = Math.abs(this.getRobot().getCoreComponent().getRootAttitude().y);
        // this.cumUnstab += roll + pitch;

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

        // Can add weighting factors for relative importance
		f1 =  (this.cumDistance)*10;
		f2 =  (this.cumAltitude)*1;
		f3 = (minPartDist)*300;
		console.log("cumdist: " + f1 + " cumalt: " + f2 + " minpartdist: " + f3);
		
        var fitness = f1 + f2 + f3;
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