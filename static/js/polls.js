const poll_edit = document.getElementsByClassName("poll-edit");
const poll_delete = document.getElementsByClassName("poll-delete");
const poll_add = document.getElementsByClassName("poll-add");

[].slice.call(poll_edit).forEach((x) =>
    x.addEventListener("mouseup", function (e) {
        const old_title = this.offsetParent.children[0].children[1];
        const old_description = this.offsetParent.children[1];
        console.log(old_title);
        console.log(old_description);
        if (old_title.nodeName == "SPAN") {
            old_title.outerHTML = `<input type="text" value="${old_title.innerText}">`;
            old_description.innerHTML = `<textarea>${old_description.innerText}</textarea>`;
        } else {
            old_title.outerHTML = `<span class="poll-title-value">${old_title.value}</span>`;
            old_description.innerHTML = `${old_description.children[0].innerHTML}`;
        }
    })
);

[].slice.call(poll_delete).forEach((x) =>
    x.addEventListener("mouseup", async function (e) {
        const poll_card = e.target.parentElement.parentElement.parentElement;
        const poll_id = this.offsetParent.children[0].children[0].innerHTML;

        const r = await fetch(`/api/delete_poll/${poll_id}`, {
            method: "DELETE",
        });
        const rJson = await r.json();

        if (rJson.status == "False") {
            alert("ERROR");
        } else {
            poll_card.remove();
        }
    })
);

[].slice.call(poll_add).forEach((x) =>
    x.addEventListener("mouseup", async function (e) {
        const poll_card = e.target.parentElement.parentElement.parentElement;
        const titleValue = poll_card.querySelector(".poll-title input").value;
        const descriptionValue = poll_card.querySelector(
            ".poll-description textarea"
        ).value;

        const r = await fetch(`/api/create_poll/`, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: titleValue,
                description: descriptionValue,
            }),
        });

        const rJson = await r.json();

        if (rJson.status == "False") {
            alert("ERROR");
        } else {
            location.reload();
        }
    })
);
