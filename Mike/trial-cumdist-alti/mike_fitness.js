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

        // Penalize vertical acceleration, roll rate, and pitch rate for stability
        this.cumUnstab = 0;

        //TODO: look at motor torques/velocities with distance

        return true;
    },

    afterSimulationStep: function() {
        // Reward cumulative travelling
        var currPos = this.getRobot().getCoreComponent().getRootPosition();
        var currDistance = this.vectorDistance(currPos, this.startPos);
        var deltaDistance = currDistance - this.prevDistance;
        if (deltaDistance > 0) {
            this.dist_progress_counter += 1;
            this.cumDistance += (deltaDistance) * this.dist_progress_counter;
        } else {
            this.dist_progress_counter = 0;
        }
        this.prevDistance = currDistance;

        // Reward cumulative climbing
        var currAltitude = this.getRobot().getCoreComponent().getRootPosition().z;
        var deltaAltitude = currAltitude - this.prevAltitude;
        if (deltaAltitude > 0) {
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

        // Can add weighting factors for relative importance
        var fitness = (this.cumDistance) + (this.cumAltitude);
        this.fitnesses.push(fitness);
        return true;
    },

    getFitness: function() {

        // Return the minimum fitness across evaluations
        fitness = this.fitnesses[0];
            for (var i = 1; i < this.fitnesses.length; i++) {
                if (this.fitnesses[i] < fitness)
                    fitness = this.fitnesses[i];
            }
        return fitness;
    },

}