

export function changeData() {
	let x = document.forms["forms"];
	let y = "" ;
	for (button in x) {
		y += button;
	}
	alert(y);
	return 1;

}
