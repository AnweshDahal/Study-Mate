itemList = document.getElementsByClassName("grid-item");
colorList = ["red-bg", "blue-bg", "yellow-bg", "purple-bg", "teal-bg"];

for (i = 0; i < itemList.length; i++) {
	itemList[i].classList.add(
		colorList[Math.floor(Math.random() * colorList.length)]
	);
}

document.addEventListener("DOMContentLoaded", function () {
	var elems = document.querySelectorAll(".sidenav");
	var instances = M.Sidenav.init(elems);
});

const switchClass = (targetName, currentClass, newClass) => {
	$(targetName).removeClass(currentClass);
	$(targetName).addClass(newClass);
};

$(window).scroll(function () {
	var scroll = $(window).scrollTop();
	if (scroll > !0) {
		switchClass("nav", "no-shadow", "shadow");
	} else {
		switchClass("nav", "shadow", "no-shadow");
	}
});

document.addEventListener("DOMContentLoaded", function () {
	var elems = document.querySelectorAll(".dropdown-trigger");
	var instances = M.Dropdown.init(elems, {
		alignment: "left",
		constraintWidth: false,
		coverTrigger: false,
	});
});

$(document).ready(function () {
	$(".tooltipped").tooltip({ exitDelay: 200 });
});

try {
	var message = document.getElementById("message").innerHTML;
} catch (err) {
	var message = "Null";
}

if (message != "Null") {
	M.toast({ html: message, displayLength: 2000 });
}
