var Singleton = (function (){
	var instance;
	function init(){
	var privateVar = "some private value"
	// Describe public variables and methods
	var publicVar = "some public value"
	var getPrivateVar = function () { return privateVar }
	var setPrivateVar = function (val) { privateVar = val; return "change value to: " + val}
	
	//return public variables and methods
	return {
	publicVar : publicVar,
	getPrivateVar : getPrivateVar,
	setPrivateVar : setPrivateVar
	}
}
	return { getInstance : function() {
			if (!instance){ 
				instance = init()
			}	
			return instance
			}
	}
})();

var firstSingletonInstance = Singleton.getInstance()
var secondSingletonInstance = Singleton.getInstance()

console.log('firstSingletonInstance.setPrivateVar("firstValue")')
firstSingletonInstance.setPrivateVar("firstValue")

console.log("firstSingletonInstance.getPrivateVar() = " + firstSingletonInstance.getPrivateVar())
console.log('\n')

console.log('secondSingletonInstance.setPrivateVar("secondValue")')
secondSingletonInstance.setPrivateVar("secondValue")
console.log("secondSingletonInstance.getPrivateVar() = " + secondSingletonInstance.getPrivateVar())
console.log(firstSingletonInstance.getPrivateVar())
