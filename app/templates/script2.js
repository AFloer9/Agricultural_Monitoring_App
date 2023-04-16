
document.querySelector(".test").addEventListener("click", changeData)

function changeData() {
	let x = document.forms.namedItem("forms");
	let y = ""
	for (let i = 0; i < 4; i++) {
		y += x[i].value
	}
	
	alert(y);
	return false;

}
