x = {
	// here we define variables for record keeping
	trialFits: [],
	direction: NaN,
	speed: 0.0005,

	// called at the beginning of the simulation
	setupSimulation: function () {
		console.log("checking light sources");
		if (this.getEnvironment().getLightSources().length == 0) {
			console.log("Error: A light source is required for the chasing scenario.");
			return false;
		}
		if (this.getEnvironment().getLightSources().length > 1) {
			console.log("Error: Only one light source is required for the chasing scenario.");
			return false;
		}

		this.getEnvironment().getLightSources()[0].setPosition(0, 0, 0.1);
		this.direction = Math.PI * Math.random();

		this.trialFits.push(0);
		this.timeSteps = 0;
		return true;
	},

	// called after each step of simulation
	afterSimulationStep: function () {
		// Compute distance from light source

		var curPos = this.getRobot().getCoreComponent().getRootPosition();

		var lightSourcePos = this.getEnvironment().getLightSources()[0].getPosition();

		this.trialFits[this.getCurTrial()] += this.vectorDistance(curPos, lightSourcePos);
		this.timeSteps++;

		// Move the light source
		var x = lightSourcePos.x + Math.sin(this.direction) * this.speed;
		var y = lightSourcePos.y + Math.cos(this.direction) * this.speed;
		this.getEnvironment().getLightSources()[0].setPosition(x, y, 0.1);

		return true;
	},


	// optional function called at the end of the simulation
	endSimulation: function () {
		// We take average distance across trial, and multiply by -1 to make
		// a maximization problem (want to be as close as possible to light
		// source at each time step)}
		console.log(this.getCurTrial());
		console.log(this.trialFits[this.getCurTrial()]);
		this.trialFits[this.getCurTrial()] *= -1 / this.timeSteps;
		console.log(this.trialFits[this.getCurTrial()]);

		return true;
	},


	// the one required method... return the fitness!
	// as usual, take minimum across trials
	getFitness: function () {
		var fitness = Number.MAX_VALUE;
		for (var i = 0; i < this.trialFits.length; i++) {
			if (this.trialFits[i] < fitness)
				fitness = this.trialFits[i];
		}
		return fitness;

	},
}