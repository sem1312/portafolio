<script>
    document.getElementById("save-btn").addEventListener("click", function () {
        const name = document.getElementById("name").textContent;
        const title = document.getElementById("title").textContent;
        const role = document.getElementById("role").textContent;
        const description = document.getElementById("description").textContent;

        alert(
            "Changes Saved!\n" +
            "Name: " + name + "\n" +
            "Title: " + title + "\n" +
            "Role: " + role + "\n" +
            "Description: " + description
        );
    });
</script>
