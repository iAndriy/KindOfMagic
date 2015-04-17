var newModule = (function(){
	// Describe private variables and methods
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
})();
console.log("newModule.privateVar=" + newModule.privateVar)
console.log("\n")
console.log("newModule.getPrivateVar()=" + newModule.getPrivateVar())
console.log("\n")
console.log(newModule.setPrivateVar("New Private Value"))
console.log(newModule.getPrivateVar())
