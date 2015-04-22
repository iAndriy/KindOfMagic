// Example 1
function Focus(){
	this.handlers = []
}

Focus.prototype.subscribe = function (handler){
		this.handlers.push(handler);
}
Focus.prototype.unsubscribe = function (handler){
	var index = this.handlers.indexOf(handler);
	if (~index){
		this.handlers.splice(index);
	}
}
Focus.prototype.notify = function (event, scopeObj){
	var scope = scopeObj || window;
	for (var i = 0; i< this.handlers.length; i++){
			this.handlers[i].call(scope, event);
	}
}

var focus = new Focus();
var firstHandler = function(message){console.log("First handler received message :" + message + "\n First handler: Go go go")};
var secondHandler = function (message) {console.log("Second handler accepted :" + message +"\n Second handler: Go go go")};

focus.subscribe(firstHandler);
focus.subscribe(secondHandler);
focus.notify('Sector Clear');
focus.unsubscribe(secondHandler);
focus.notify('Sector Clear');

// Example 2
function Observer(){
	this.listeners = [];
	
	this.subscribe = function(listener){
		this.listeners.push(listener)
	};
	this.unsubscribe = function (listener){
		var index = this.listeners.indexOf(listener);
		if (~index){
			this.listeners.splice(index, 1);
		} 
	};
	this.notify = function (event){
		for (var i = 0; i< this.listeners.length; i++){
			if (this.listeners[i][event]){
				this.listeners[i][event].call(this.listeners[i]);
			}
		}
	}
}

function DisneylandAnimal(name){
	this.name = name;
	this.freeNuts = function (){
		console.log(this.name + ": Where free nuts?");
	}
}
var observer = new Observer();
var chip = new DisneylandAnimal('Chip');
var dale = new DisneylandAnimal('Dale');
observer.subscribe(chip);
observer.subscribe(dale);
observer.notify('freeNuts');
observer.unsubscribe(chip);
observer.notify('freeNuts');



