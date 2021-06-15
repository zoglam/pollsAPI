const poll_edit = document.getElementsByClassName("poll-edit");
const poll_delete = document.getElementsByClassName("poll-delete");
const poll_add = document.getElementsByClassName("poll-add");

[].slice.call(poll_edit).forEach((x) =>
    x.addEventListener("mouseup", function (e) {
        const old_title = this.offsetParent.children[0].children[1];
        const old_description = this.offsetParent.children[1];
        console.log(old_title);
        console.log(old_description);
        const input_title = document.createElement("input");
        input_title.value = old_title.innerHTML;
        console.log(old_title.innerHTML);
        console.log(input_title);
        old_title.outerHTML = input_title.outerHTML;
    })
);
