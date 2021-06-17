const question_delete = document.getElementsByClassName("question-delete");
const question_add = document.getElementsByClassName("question-add");

[].slice.call(question_delete).forEach((x) =>
    x.addEventListener("mouseup", async function (e) {
        const row = e.target.parentElement.parentElement;
        const question_id = row.querySelector('th').innerHTML

        const r = await fetch(`/api/delete_question/${question_id}`, {
            method: "DELETE",
        });
        const rJson = await r.json();

        if (rJson.status == "False") {
            alert("ERROR");
        } else {
            row.remove();
        }
    })
);

[].slice.call(question_add).forEach((x) =>
    x.addEventListener("mouseup", async function (e) {
        const row = e.target.parentElement.parentElement;
        const title = row.querySelector("input");
        const type = row.querySelectorAll("select")[0];
        const poll_id = row.querySelectorAll("select")[1];

        const r = await fetch(`/api/create_question/`, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_poll: poll_id.value,
                title: title.value,
                question_type: type.value,
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
