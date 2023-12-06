let pillButtonOnText = document.querySelector(".pill-button-selection_on"),
    pillButtonOffText = document.querySelector(".pill-button-selection_off"),
    pillButtonHighlight = document.querySelector(".pill-button-highlight"),
    pillButtonOnTextWidth = pillButtonOnText.offsetWidth,
    pillButtonOffTextWidth = pillButtonOffText.offsetWidth,
    pillButtonOnTextPosition = {
        left: pillButtonOnText.offsetLeft,
    },
    pillButtonOffTextPosition = {
        left: pillButtonOffText.offsetLeft,
    },
    pillButtonInput = document.querySelector(".pill-button-input"),
    configureDiv = document.querySelector("#configureDiv"),
    generateDiv = document.querySelector("#generateDiv");

pillButtonHighlight.style.width = pillButtonOnTextWidth + "px";

document.querySelectorAll(".pill-button-selection").forEach(function (button) {
    button.addEventListener("click", function () {
        if (!this.classList.contains("pill-button-selection_active")) {
            document
                .querySelectorAll(".pill-button-selection")
                .forEach(function (element) {
                    element.classList.remove("pill-button-selection_active");
                });
            this.classList.add("pill-button-selection_active");

            if (
                this.classList.contains("pill-button-selection_off") &&
                pillButtonInput.checked
            ) {
                pillButtonInput.checked = false;
                configureDiv.style.display = "none";
                generateDiv.style.display = "flex";
                pillButtonHighlight.style.width = pillButtonOffTextWidth + "px";
                pillButtonHighlight.style.left =
                    pillButtonOffTextPosition.left + "px";
            } else {
                pillButtonInput.checked = true;
                configureDiv.style.display = "flex";
                generateDiv.style.display = "none";
                pillButtonHighlight.style.width = pillButtonOnTextWidth + "px";
                pillButtonHighlight.style.left =
                    pillButtonOnTextPosition.left + "px";
            }
        }
    });
});

if (pillButtonInput.checked) {
    pillButtonHighlight.style.width = pillButtonOnTextWidth + "px";
    configureDiv.style.display = "flex";
    generateDiv.style.display = "none";
} else {
    pillButtonHighlight.style.width = pillButtonOffTextWidth + "px";
    configureDiv.style.display = "none";
    generateDiv.style.display = "flex";
}

// next and previous button logic for configure
const nextC = document.getElementById("nextC"),
    previousC = document.getElementById("previousC"),
    step1C = document.getElementById("step1C"),
    step2C = document.getElementById("step2C"),
    step3C = document.getElementById("step3C"),
    step1HeadingC = document.getElementById("step1HeadingC"),
    step2HeadingC = document.getElementById("step2HeadingC");

hideAllStepsC = () => {
    step1C.classList.add("hidden");
    step2C.classList.add("hidden");
    step3C.classList.add("hidden");

    step1HeadingC.children[0].classList.remove("bg-primaryPurple");
    step2HeadingC.children[0].classList.remove("bg-primaryPurple");

    step1HeadingC.children[0].classList.remove("bg-secondaryPurple");
    step2HeadingC.children[0].classList.remove("bg-secondaryPurple");

    step1HeadingC.children[1].children[0].classList.remove("font-bold");
    step2HeadingC.children[1].children[0].classList.remove("font-bold");

    step1HeadingC.children[1].children[0].classList.remove("underline");
    step2HeadingC.children[1].children[0].classList.remove("underline");

    step1HeadingC.children[1].children[0].classList.remove("line-through");
    step2HeadingC.children[1].children[0].classList.remove("line-through");

    step1HeadingC.children[1].children[1].classList.add("hidden");
    step2HeadingC.children[1].children[1].classList.add("hidden");
};
let currentStepC = 1;
updateStepC = () => {
    hideAllStepsC();
    switch (currentStepC) {
        case 1:
            step1C.classList.remove("hidden");
            step1HeadingC.children[1].children[0].classList.add("underline");
            step1HeadingC.children[1].children[0].classList.add("font-bold");
            step1HeadingC.children[0].classList.add("bg-primaryPurple");
            break;
        case 2:
            step2C.classList.remove("hidden");
            step2HeadingC.children[1].children[0].classList.add("underline");
            step2HeadingC.children[1].children[0].classList.add("font-bold");
            step2HeadingC.children[0].classList.add("bg-primaryPurple");
            break;
        case 3:
            step3C.classList.remove("hidden");
            break;
    }

    for (let i = 1; i < currentStepC; i++) {
        document
            .getElementById(`step${i}HeadingC`)
            .children[0].classList.add("bg-secondaryPurple");
        document
            .getElementById(`step${i}HeadingC`)
            .children[1].children[0].classList.remove("underline");
        document
            .getElementById(`step${i}HeadingC`)
            .children[1].children[0].classList.remove("font-bold");
        document
            .getElementById(`step${i}HeadingC`)
            .children[1].children[0].classList.add("line-through");
        document
            .getElementById(`step${i}HeadingC`)
            .children[1].children[1].classList.remove("hidden");
        document.getElementById(
            `step${i}HeadingC`
        ).children[1].children[1].textContent =
            formDataC[Object.keys(formDataC)[i - 1]];
    }
};

const tableBody = document.getElementById("tableBody");
function tableBodyContent() {
    // query the backend to check availability of result for semester
    const course = formDataC.course.split(" ")[0];
    const shift = formDataC.course.split(" ").pop() === "Morning" ? 1 : 2;
    const details = {
        course: course,
        passing: formDataC.year,
        shift: shift,
    };

    // making the call to the backend
    let available_semesters = null;
    fetch("http://localhost:8000/results/check-result/", {
        method: "POST",
        body: JSON.stringify(details),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            available_semesters = Object.keys(data);
            // add rows in the table
            const numberOfSem = semesterByCourse[formDataC.course];
            for (let i = 0; i < numberOfSem; i++) {
                const tr = document.createElement("tr");
                const td1 = document.createElement("td");
                td1.textContent = `Semester ${i + 1}`;
                const td2 = document.createElement("td");
                const td3 = document.createElement("td");

                td1.classList.add("border", "px-4", "py-2");
                td2.classList.add("border", "px-4", "py-2");
                td3.classList.add("border", "px-4", "py-2");

                // logic for adding upload/download button depending on the data recevied from the backend
                if (available_semesters.includes(String(i + 1))) {
                    // download button
                    const downloadBtn = document.createElement("button");
                    const link = document.createElement("a");
                    link.href = `/results/download-result/${data[i + 1]}`;
                    link.classList.add("bg-primaryPurple", "text-white", "p-2");
                    link.textContent = "Download";
                    downloadBtn.appendChild(link);
                    td3.appendChild(downloadBtn);

                    // update button
                    const form = document.createElement("form");
                    const fileInput = document.createElement("input");

                    fileInput.setAttribute("type", "file");
                    fileInput.setAttribute("name", "updated_result");
                    fileInput.setAttribute("accept", ".xlsx");
                    fileInput.setAttribute("required", "true");
                    fileInput.setAttribute("id", "updated_result");

                    const updateBtn = document.createElement("button");
                    updateBtn.setAttribute("type", "submit");
                    updateBtn.setAttribute("id", "updateBtn");
                    updateBtn.classList.add(
                        "bg-primaryPurple",
                        "text-white",
                        "p-2"
                    );
                    updateBtn.textContent = "Update";
                    form.addEventListener("submit", function (event) {
                        event.preventDefault();
                        update_result(i + 1, details);
                    });
                    form.appendChild(fileInput);
                    form.appendChild(updateBtn);
                    td2.appendChild(form);
                } else {
                    const form = document.createElement("form");
                    const fileInput = document.createElement("input");
                    fileInput.setAttribute("type", "file");
                    fileInput.setAttribute("id", `excel-${i + 1}`);
                    fileInput.setAttribute("accept", ".csv");
                    fileInput.setAttribute("required", "true");
                    fileInput.setAttribute("name", "excelfile");

                    const uploadBtn = document.createElement("button");
                    uploadBtn.setAttribute("type", "submit");
                    uploadBtn.setAttribute("id", `btn-${i + 1}`);
                    uploadBtn.classList.add(
                        "bg-primaryPurple",
                        "text-white",
                        "p-2"
                    );
                    uploadBtn.textContent = "Upload";
                    form.addEventListener("submit", function (event) {
                        event.preventDefault();
                        upload_excel(i + 1, details);
                    });

                    form.appendChild(fileInput);
                    form.appendChild(uploadBtn);
                    td2.appendChild(form);
                }

                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);

                tableBody.appendChild(tr);
            }
        })
        .catch((err) => console.log(err));
}

async function upload_excel(semester, details) {
    const course = formDataC.course.split(" ")[0];
    // headers to add
    const courseLength = `${
        formDataC.year - semesterByCourse[formDataC.course] / 2
    } - ${formDataC.year}`;
    let headers_to_add = [
        ["Maharaja Surajmal Institute"],
        [`${formDataC.course} Batch ${courseLength}`],
        [`Class-: ${course}  ${semester} Semester Batch [${courseLength}]`],
    ];
    // footers to add
    const footers_to_add = await get_footers(details, semester);
    const file_to_be_uploaded = document.getElementById(`excel-${semester}`)
        .files[0];
    const formData = new FormData();
    formData.append("excel_file", file_to_be_uploaded); // 'excel_file' is the name you will use on the server to access the file
    formData.append("course", details.course);
    formData.append("passing", details.passing);
    formData.append("shift", details.shift);
    formData.append("semester", semester);
    formData.append("headers_to_add", JSON.stringify(headers_to_add));
    formData.append("footers_to_add", JSON.stringify(footers_to_add));
    fetch("http://localhost:8000/results/normalize/", {
        method: "POST",
        body: formData, // Use FormData as the request body
    })
        .then((response) => {
            tableBody.innerHTML = "";
            tableBodyContent();
        })
        .catch((err) => {
            console.log(err);
        });
}

const closeFooterModal = document.getElementById("closeFooterModal"),
    addInputOption = document.getElementById("addInputOption"),
    footersModal = document.getElementById("footers_modal"),
    backdrop = document.getElementById("backdrop"),
    footerHeader = document.getElementById("footers_modal").children[0],
    footerBody = document.getElementById("footers_modal").children[1],
    footerForm = document.getElementById("footerForm").children[0],
    saveFooterModal = document.getElementById("submitFooterModal");

closeFooterModal.addEventListener("click", function () {
    backdrop.classList.add("hidden");
    footersModal.classList.add("hidden");
});

addInputOption.addEventListener("click", function () {
    footerForm.appendChild(getInputOption());
});

async function get_footers(details, semester) {
    backdrop.classList.remove("hidden");
    footersModal.classList.remove("hidden");

    footerHeader.innerHTML = `${formDataC.course} Semester ${semester}`;

    const footerFormSubmit = document.getElementById("footerForm");
    const footers = new Promise((resolve) => {
        footerFormSubmit.addEventListener("submit", function (event) {
            event.preventDefault();
            const inputs = footerForm.children;
            const footers = [];
            for (let i = 0; i < inputs.length; i++) {
                const input = inputs[i].children;
                const footer = [];
                let str = "";
                for (let j = 0; j < input.length; j++) {
                    str += input[j].value + " ";
                    input[j].value = "";
                }
                str = str.trim();
                footer.push(str);
                footers.push(footer);
            }
            backdrop.classList.add("hidden");
            footersModal.classList.add("hidden");
            resolve(footers);
        });
    });

    const footers_to_add = await footers;
    return footers_to_add;
}

function getInputOption() {
    const div = document.createElement("div");
    div.classList.add("flex", "gap-4", "items-center");
    const code = document.createElement("input");
    code.setAttribute("type", "text");
    code.setAttribute("placeholder", "Subject Code");
    code.classList.add("border", "border-gray", "p-2", "rounded-md");
    const name = document.createElement("input");
    name.setAttribute("type", "text");
    name.setAttribute("placeholder", "Subject Name");
    name.classList.add("border", "border-gray", "p-2", "rounded-md");
    const teacher = document.createElement("input");
    teacher.setAttribute("type", "text");
    teacher.setAttribute("placeholder", "Teacher Name");
    teacher.classList.add("border", "border-gray", "p-2", "rounded-md");

    div.appendChild(code);
    div.appendChild(name);
    div.appendChild(teacher);

    return div;
}

function update_result(semester, details) {
    const file_to_be_uploaded =
        document.getElementById("updated_result").files[0];

    const formData = new FormData();
    formData.append("updated_excel_file", file_to_be_uploaded); // 'updated_excel_file' is the name you will use on the server to access the file
    formData.append("course", details.course);
    formData.append("passing", details.passing);
    formData.append("shift", details.shift);
    formData.append("semester", semester);

    fetch("http://localhost:8000/results/update-result/", {
        method: "POST",
        body: formData, // Use FormData as the request body
    })
        .then((response) => {
            tableBody.innerHTML = "";
            tableBodyContent();
        })
        .catch((err) => {
            console.log(err);
        });
}

nextC.addEventListener("click", function () {
    previousC.classList.remove("invisible");
    if (currentStepC <= 3) {
        currentStepC < 3 && currentStepC++;
        if (currentStepC === 3) {
            nextC.classList.add("invisible");
            tableBodyContent();
        } else {
            nextC.classList.remove("invisible");
        }
        updateStepC();
    }
});

previousC.addEventListener("click", function () {
    nextC.classList.remove("invisible");
    tableBody.innerHTML = "";
    if (currentStepC > 1) {
        currentStepC--;
        currentStepC === 1
            ? previousC.classList.add("invisible")
            : previousC.classList.remove("invisible");
        updateStepC();
    }
});

// next and previous button logic for generate
const next = document.getElementById("next"),
    previous = document.getElementById("previous"),
    generate = document.getElementById("generate"),
    download = document.getElementById("download"),
    step1 = document.getElementById("step1"),
    step2 = document.getElementById("step2"),
    step3 = document.getElementById("step3"),
    step4 = document.getElementById("step4"),
    step5 = document.getElementById("step5"),
    previewDiv = document.getElementById("preview"),
    step1Heading = document.getElementById("step1Heading"),
    step2Heading = document.getElementById("step2Heading"),
    step3Heading = document.getElementById("step3Heading"),
    step4Heading = document.getElementById("step4Heading"),
    step5Heading = document.getElementById("step5Heading");

hideAllSteps = () => {
    step1.classList.add("hidden");
    step2.classList.add("hidden");
    step3.classList.add("hidden");
    step4.classList.add("hidden");
    step5.classList.add("hidden");
    previewDiv.classList.add("hidden");

    step1Heading.children[0].classList.remove("bg-primaryPurple");
    step2Heading.children[0].classList.remove("bg-primaryPurple");
    step3Heading.children[0].classList.remove("bg-primaryPurple");
    step4Heading.children[0].classList.remove("bg-primaryPurple");
    step5Heading.children[0].classList.remove("bg-primaryPurple");

    step1Heading.children[0].classList.remove("bg-secondaryPurple");
    step2Heading.children[0].classList.remove("bg-secondaryPurple");
    step3Heading.children[0].classList.remove("bg-secondaryPurple");
    step4Heading.children[0].classList.remove("bg-secondaryPurple");
    step5Heading.children[0].classList.remove("bg-secondaryPurple");

    step1Heading.children[1].children[0].classList.remove("font-bold");
    step2Heading.children[1].children[0].classList.remove("font-bold");
    step3Heading.children[1].children[0].classList.remove("font-bold");
    step4Heading.children[1].children[0].classList.remove("font-bold");
    step5Heading.children[1].children[0].classList.remove("font-bold");

    step1Heading.children[1].children[0].classList.remove("underline");
    step2Heading.children[1].children[0].classList.remove("underline");
    step3Heading.children[1].children[0].classList.remove("underline");
    step4Heading.children[1].children[0].classList.remove("underline");
    step5Heading.children[1].children[0].classList.remove("underline");

    step1Heading.children[1].children[0].classList.remove("line-through");
    step2Heading.children[1].children[0].classList.remove("line-through");
    step3Heading.children[1].children[0].classList.remove("line-through");
    step4Heading.children[1].children[0].classList.remove("line-through");
    step5Heading.children[1].children[0].classList.remove("line-through");

    step1Heading.children[1].children[1].classList.add("hidden");
    step2Heading.children[1].children[1].classList.add("hidden");
    step3Heading.children[1].children[1].classList.add("hidden");
    step4Heading.children[1].children[1].classList.add("hidden");
    step5Heading.children[1].children[1].classList.add("hidden");
};

updateStep = () => {
    hideAllSteps();
    switch (currentStep) {
        case 1:
            step1.classList.remove("hidden");
            step1Heading.children[1].children[0].classList.add("underline");
            step1Heading.children[1].children[0].classList.add("font-bold");
            step1Heading.children[0].classList.add("bg-primaryPurple");
            break;
        case 2:
            step2.classList.remove("hidden");
            step2Heading.children[1].children[0].classList.add("underline");
            step2Heading.children[1].children[0].classList.add("font-bold");
            step2Heading.children[0].classList.add("bg-primaryPurple");
            break;
        case 3:
            step3.classList.remove("hidden");
            step3Heading.children[1].children[0].classList.add("underline");
            step3Heading.children[1].children[0].classList.add("font-bold");
            step3Heading.children[0].classList.add("bg-primaryPurple");
            break;
        case 4:
            step4.classList.remove("hidden");
            step4Heading.children[1].children[0].classList.add("font-bold");
            step4Heading.children[1].children[0].classList.add("underline");
            step4Heading.children[0].classList.add("bg-primaryPurple");
            break;
        case 5:
            step5.classList.remove("hidden");
            step5Heading.children[1].children[0].classList.add("font-bold");
            step5Heading.children[1].children[0].classList.add("underline");
            step5Heading.children[0].classList.add("bg-primaryPurple");
            break;
        case 6:
            previewDiv.classList.remove("hidden");
            break;
    }

    for (let i = 1; i < currentStep; i++) {
        document
            .getElementById(`step${i}Heading`)
            .children[0].classList.add("bg-secondaryPurple");
        document
            .getElementById(`step${i}Heading`)
            .children[1].children[0].classList.remove("underline");
        document
            .getElementById(`step${i}Heading`)
            .children[1].children[0].classList.remove("font-bold");
        document
            .getElementById(`step${i}Heading`)
            .children[1].children[0].classList.add("line-through");
        document
            .getElementById(`step${i}Heading`)
            .children[1].children[1].classList.remove("hidden");
        document.getElementById(
            `step${i}Heading`
        ).children[1].children[1].textContent =
            i >= 3
                ? formData[Object.keys(formData)[i - 1]][entryNumber - 1]
                : formData[Object.keys(formData)[i - 1]];
    }
};

let entrySelected = 1;
// format 1 and 6
function multipleEntries() {
    for (let i = 0; i < entryNumber; i++) {
        const div = document.createElement("div");
        div.classList.add(
            "flex",
            "flex-col",
            "bg-gray2",
            "text-white",
            "p-2",
            "rounded-md",
            "relative",
            "cursor-pointer"
        );
        div.setAttribute("id", `entryHeader${i + 1}`);
        // data
        for (let j = 2; j < 5; j++) {
            const p = document.createElement("p");
            p.classList.add("text-lg");
            p.textContent = formData[Object.keys(formData)[j]][i];
            div.appendChild(p);
        }
        // cancel img
        const cancelImg = document.createElement("img");
        cancelImg.src = "/static/cancel.svg";
        cancelImg.alt = "cancel";
        cancelImg.classList.add(
            "cursor-pointer",
            "absolute",
            "-top-2",
            "-right-2"
        );
        div.appendChild(cancelImg);
        cancelImg.addEventListener("click", (event) => deleteEntry(event));
        cancelImg.setAttribute("id", `cancel${i + 1}`);

        div.addEventListener("click", () => {
            entrySelected = div.id[div.id.length - 1];
            updateEntry();
        });
        previewHeader.appendChild(div);
    }
    updateEntry();
}
// format 2 and 7
function singleEntry() {
    const div = document.createElement("div");
    div.classList.add(
        "flex",
        "gap-3",
        "bg-gray2",
        "text-white",
        "p-2",
        "rounded-md",
        "relative",
        "cursor-pointer"
    );
    div.setAttribute("id", "entryHeader1");
    // data
    for (let j = 2; j < 5; j++) {
        const p = document.createElement("p");
        p.classList.add("text-lg");
        p.textContent = formData[Object.keys(formData)[j]][0];
        div.appendChild(p);
    }
    div.addEventListener("click", () => {
        entrySelected = div.id[div.id.length - 1];
        updateEntry();
    });
    previewHeader.appendChild(div);
    updateEntry();
}
async function previewDivDetails() {
    const previewHeader = document.getElementById("previewHeader");
    previewHeader.innerHTML = "";
    if (
        formData.course.length < 1 &&
        formData.semester.length < 1 &&
        formData.year.length < 1
    ) {
        alert("Please fill all the fields");
        return;
    }
    await updatePreview();
}
function updateEntry() {
    for (let i = 1; i <= entryNumber; i++) {
        const entryHeader = document.getElementById(`entryHeader${i}`);
        const entryBody = document.getElementById(`entry${i}`);
        entryBody.classList.add("hidden");
        entryHeader.classList.remove("bg-primaryPurple");
        entryHeader.classList.add("bg-gray2");
        if (i == entrySelected) {
            entryBody.classList.remove("hidden");
            entryHeader.classList.remove("bg-gray2");
            entryHeader.classList.add("bg-primaryPurple");
        }
    }
}

async function updatePreview() {
    const previewBody = document.getElementById("previewBody");
    previewBody.innerHTML = "";
    const div = document.createElement("div");
    const entryDiv = document.createElement("div");
    const section = document.createElement("input");
    const faculty_name = document.createElement("input");
    const semester = formData.semester[0].split(" ")[1];
    const course = formData.course[0].split(" ")[0];
    switch (Number(formData.format_number)) {
        case 1:
            // for body
            div.setAttribute("id", "format1");
            for (let i = 0; i < entryNumber; i++) {
                entryDiv.setAttribute("id", `entry${i + 1}`);
                entryDiv.classList.add("flex", "flex-col", "gap-4");
                const name = document.createElement("input");
                name.classList.add(
                    "border",
                    "border-gray",
                    "p-2",
                    "rounded-md"
                );
                name.setAttribute("type", "text");
                name.setAttribute("placeholder", "Faculty Name");
                const section = document.createElement("input");
                section.classList.add(
                    "border",
                    "border-gray",
                    "p-2",
                    "rounded-md"
                );
                section.setAttribute("type", "text");
                section.setAttribute("placeholder", "Section");
                const subjectCodes = document.createElement("select");
                subjectCodes.classList.add("chosen-select");
                subjectCodes.setAttribute("id", `subject_codes${i + 1}`);
                subjectCodes.multiple = true;
                subjectCodes.setAttribute(
                    "data-placeholder",
                    "Select Subject Codes"
                );
                // getting the options from backend
                fetch(
                    `http://127.0.0.1:8000/results/format1/?course=${
                        formData.course[i].split(" ")[0]
                    }&semester=${formData.semester[i].split(" ")[1]}`
                )
                    .then((res) => res.json())
                    .then((data) => {
                        for (let [key, value] of Object.entries(data)) {
                            const option = document.createElement("option");
                            option.value = key;
                            option.textContent = value;
                            subjectCodes.appendChild(option);
                        }
                    });

                entryDiv.appendChild(name);
                entryDiv.appendChild(section);
                entryDiv.appendChild(subjectCodes);
                div.appendChild(entryDiv);
            }
            previewBody.appendChild(div);
            // for header
            multipleEntries();
            await fetchSubjectCodes();
            // chosen
            for (let i = 0; i < entryNumber; i++) {
                console.log(document.getElementById(`subject_codes${i + 1}`));
                $(`#subject_codes${i + 1}`).chosen();
            }
            break;
        case 2:
            div.setAttribute("id", "format2");
            document.getElementById("addEntry").classList.add("hidden");
            entryDiv.setAttribute("id", "entry1");
            entryDiv.classList.add("flex", "flex-col", "gap-4");
            section.setAttribute("type", "text");
            section.setAttribute("id", "Section");
            section.classList.add("border", "border-gray", "p-2", "rounded-md");
            section.placeholder = "Section";
            entryDiv.appendChild(section);
            faculty_name.setAttribute("id", "faculty_name");
            faculty_name.classList.add(
                "border",
                "border-gray",
                "p-2",
                "rounded-md"
            );
            faculty_name.placeholder = "Class Co-ordinator Name";
            faculty_name.setAttribute("type", "text");
            entryDiv.appendChild(faculty_name);
            // gettting data from backend

            fetch(
                `http://127.0.0.1:8000/results/format2/?semester=${semester}&course=${course}`
            )
                .then((res) => res.json())
                .then((data) => {
                    for (let [key, value] of Object.entries(data[1])) {
                        const subjectEntry = document.createElement("div");
                        subjectEntry.classList.add(
                            "flex",
                            "justify-between",
                            "items-center"
                        );
                        const p = document.createElement("p");
                        p.classList.add("text-lg", "font-bold");
                        p.setAttribute("id", key);
                        p.textContent = value;
                        const input = document.createElement("input");
                        input.classList.add(
                            "border",
                            "border-gray",
                            "p-2",
                            "rounded-md"
                        );
                        input.setAttribute("type", "text");
                        input.placeholder = "Enter Faculty Name";
                        subjectEntry.appendChild(p);
                        subjectEntry.appendChild(input);
                        entryDiv.appendChild(subjectEntry);
                    }
                });
            previewBody.appendChild(entryDiv);
            // for header
            singleEntry();
            break;
        case 6:
            div.setAttribute("id", "format6");
            div.innerHTML = "format6";
            break;
        case 7:
            div.setAttribute("id", "format7");
            document.getElementById("addEntry").classList.add("hidden");
            entryDiv.setAttribute("id", "entry1");
            entryDiv.classList.add("flex", "flex-col", "gap-4");
            section.setAttribute("type", "text");
            section.setAttribute("id", "Section");
            section.classList.add("border", "border-gray", "p-2", "rounded-md");
            section.placeholder = "Section";
            entryDiv.appendChild(section);
            faculty_name.setAttribute("id", "faculty_name");
            faculty_name.classList.add(
                "border",
                "border-gray",
                "p-2",
                "rounded-md"
            );
            faculty_name.placeholder = "Class Co-ordinator Name";
            faculty_name.setAttribute("type", "text");
            entryDiv.appendChild(faculty_name);
            // getting data from backend
            fetch(
                `http://127.0.0.1:8000/results/format7/?semester=${semester}&course=${course}`
            )
                .then((res) => res.json())
                .then((data) => {
                    for (let [key, value] of Object.entries(data.Subjects)) {
                        const subjectEntry = document.createElement("div");
                        subjectEntry.classList.add(
                            "flex",
                            "justify-between",
                            "items-center"
                        );
                        const p = document.createElement("p");
                        p.classList.add("text-lg", "font-bold");
                        p.setAttribute("id", key);
                        p.textContent = value;
                        Object.keys(data.Practicals).forEach((practicalKey) => {
                            if (key === practicalKey) {
                                p.setAttribute("name", "practical");
                            }
                        });
                        const input = document.createElement("input");
                        input.classList.add(
                            "border",
                            "border-gray",
                            "p-2",
                            "rounded-md"
                        );
                        input.setAttribute("type", "text");
                        input.placeholder = "Enter Faculty Name";
                        subjectEntry.appendChild(p);
                        subjectEntry.appendChild(input);
                        entryDiv.appendChild(subjectEntry);
                    }
                });
            previewBody.appendChild(entryDiv);
            // for header
            singleEntry();
            break;
    }
}
async function fetchSubjectCodes() {
    let promises = [];

    for (let i = 0; i < entryNumber; i++) {
        const select = document.getElementById(`subject_codes${i + 1}`);
        select.classList.remove("hidden");
        select.classList.add("chosen-select");

        let promise = fetch(
            `http://127.0.0.1:8000/results/format1/?course=${
                formData.course[i].split(" ")[0]
            }&semester=${formData.semester[i].split(" ")[1]}`
        )
            .then((res) => res.json())
            .then((data) => {
                for (let [key, value] of Object.entries(data)) {
                    const option = document.createElement("option");
                    option.value = key;
                    option.textContent = value;
                    select.appendChild(option);
                }
            });

        promises.push(promise);
    }

    await Promise.all(promises);
}

function deleteEntry(event) {
    event.stopPropagation();
    entryNumber--;
    event.target.parentElement.remove();
    const id = event.target.id[event.target.id.length - 1];
    document.getElementById(`entry${id}`).remove();

    for (let i = 2; i < 5; i++) {
        formData[Object.keys(formData)[i]].splice(id - 1, 1);
    }
    if (entryNumber === 0) {
        entryNumber = 1;
        currentStep = 3;
        updateStep();
        next.classList.remove("invisible");
        generate.classList.add("hidden");
        document.getElementById("selected").classList.remove("hidden");

        const courseArr = Array.from(step3.children[2].children);
        courseArr.forEach((element) =>
            element.classList.remove("select__item--selected")
        );
    }
}

const addEntry = document.getElementById("addEntry");
addEntry.addEventListener("click", () => {
    if (
        formData.course.length >= 1 &&
        formData.semester.length >= 1 &&
        formData.year.length >= 1
    ) {
        entryNumber++;
        details = {};
        currentStep = 3;
        updateStep();
        next.classList.remove("invisible");
        generate.classList.add("hidden");
        download.classList.add("hidden");
        document.getElementById("selected").classList.remove("hidden");

        const courseArr = Array.from(step3.children[2].children);
        courseArr.forEach((element) =>
            element.classList.remove("select__item--selected")
        );
    } else {
        alert("Please fill all the fields");
    }
});

let currentStep = 1,
    entryNumber = 1;
next.addEventListener("click", async function () {
    const selected = document.getElementById("selected");
    if (formData[Object.keys(formData)[currentStep]]) {
        if (currentStep >= 3) {
            selected.innerHTML = formData[Object.keys(formData)[currentStep]][
                entryNumber - 1
            ]
                ? `Selected: ${
                      formData[Object.keys(formData)[currentStep]][
                          entryNumber - 1
                      ]
                  }`
                : "Selected: ";
        } else {
            selected.innerHTML = `Selected: ${
                formData[Object.keys(formData)[currentStep]]
            }`;
        }
    } else {
        selected.innerHTML = "Selected: ";
    }
    previous.classList.remove("invisible");
    if (currentStep <= 6) {
        currentStep < 6 && currentStep++;
        if (currentStep === 6) {
            document.getElementById("selected").classList.add("hidden");
            generate.classList.remove("hidden");
            next.classList.add("invisible");
            step5.classList.add("hidden");
            previewDiv.classList.remove("hidden");
            await previewDivDetails();
        } else {
            next.classList.remove("invisible");
        }
        updateStep();
    }
});

previous.addEventListener("click", function () {
    next.classList.remove("invisible");
    previewDiv.classList.add("hidden");
    generate.classList.add("hidden");
    download.classList.add("hidden");
    document.getElementById("selected").innerHTML = `Selected: ${
        formData[Object.keys(formData)[currentStep - 2]]
    }`;
    document.getElementById("selected").classList.remove("hidden");

    if (currentStep > 1) {
        currentStep--;
        currentStep === 1
            ? previous.classList.add("invisible")
            : previous.classList.remove("invisible");
        if (currentStep === 6) {
            next.classList.add("invisible");
            generate.classList.remove("hidden");
        }
        updateStep();
    }
});

let details = {};
generate.addEventListener("click", function () {
    currentStep < 6 && currentStep++;
    updateStep();
    switch (Number(formData.format_number)) {
        case 1:
            format1();
            break;
        case 2:
            format2();
            break;
        case 6:
            format6();
            break;
        case 7:
            format7();
            break;
    }

    generate.classList.add("hidden");
    download.classList.remove("hidden");
});

function format2() {
    details.course = formData.course[0].split(" ")[0];
    details.shift = formData.course[0].split(" ").pop() != "Morning" ? 2 : 1;
    details.semester = Number(formData.semester[0].split(" ")[1]);
    details.passing = Number(formData.year[0]);
    details.section = String(
        document.getElementById("Section").value
    ).toUpperCase();
    details.faculty_name = document.getElementById("faculty_name").value;
    const yearDiff = semesterByCourse[formData.course[0]] / 2;
    details.batch = `${details.passing - yearDiff} - ${details.passing}`;

    let subjectTeacherMapping = {};

    const entries = Array.from(document.getElementById("entry1").children);
    entries.splice(0, 2);
    entries.forEach((entry) => {
        subjectTeacherMapping[entry.children[0].id] = entry.children[1].value;
    });
    details.subjectTeacherMapping = subjectTeacherMapping;
    console.log("format2", details);
}

function format7() {
    const yearDiff = semesterByCourse[formData.course[0]] / 2;
    details.Section = String(
        document.getElementById("Section").value
    ).toUpperCase();
    details.faculty_name = document.getElementById("faculty_name").value;
    details.semester = Number(formData.semester[0].split(" ")[1]);
    details.shift = formData.course[0].split(" ").pop() != "Morning" ? 2 : 1;
    details.passing = Number(formData.year[0]);
    details.admitted = Number(formData.year[0] - yearDiff);
    details.course = formData.course[0].split(" ")[0];
    let Subjects = [],
        Practicals = [];
    let names = [];
    const entries = Array.from(document.getElementById("entry1").children);
    entries.splice(0, 2);
    entries.forEach((entry) => {
        Subjects.push(entry.children[0].id);
        names.push(entry.children[1].value);
        if (
            entry.children[0].hasAttribute("name") &&
            entry.children[0].getAttribute("name") === "practical"
        )
            Practicals.push(entry.children[0].id);
    });
    details.Subjects = Subjects;
    details.Practicals = Practicals;
    details["Faculty Names"] = names;

    console.log("format7", details);
}

function format1() {
    let shift = [];
    let faculty_name = [];
    for (let i = 0; i < formData.course.length; i++) {
        shift.push(formData.course[i].split(" ").pop() != "Morning" ? 2 : 1);
        faculty_name.push(
            document.getElementById(`entry${i + 1}`).children[0].value
        );
    }
    if (!shift.every((val) => val === shift[0])) {
        alert("Please select same shift for all the courses");
        download.classList.add("hidden");
        generate.classList.remove("hidden");
        return;
    }
    if (!faculty_name.every((val) => val === faculty_name[0])) {
        alert("Please select same faculty for all the entries");
        download.classList.add("hidden");
        generate.classList.remove("hidden");
        return;
    }
    for (let i = 0; i < entryNumber; i++) {
        const semester = formData.semester[i].split(" ")[1];
        const passing = formData.year[i];
        const course = formData.course[i].split(" ")[0];

        const section = String(
            document.getElementById(`entry${i + 1}`).children[1].value
        ).toUpperCase();
        let flag = 0;

        for (let j = 0; j < Object.keys(details).length; j++) {
            if (
                details[j].semester == semester &&
                details[j].passing == passing &&
                details[j].course == course
            ) {
                console.log("inside if");
                let subjectCodes = [];
                subjectCodes.push(
                    ...$(
                        document.getElementById(`entry${i + 1}`).children[2]
                    ).val()
                );
                details[j]["section-subject"][section] = subjectCodes;
                flag = 1;
                break;
            }
        }

        if (flag) continue;
        console.log("outside for");
        let entry = {
            semester: Number(semester),
            passing,
            course,
            "section-subject": {},
            faculty_name: faculty_name[0],
            shift: shift[0],
        };
        let subjectCodes = [];
        subjectCodes.push(
            ...$(document.getElementById(`entry${i + 1}`).children[2]).val()
        );
        entry["section-subject"][section] = subjectCodes;
        details[i] = entry;
    }
    console.log(details);
}

download.addEventListener("click", function () {
    // handle download
    switch (Number(formData.format_number)) {
        case 1:
            Initiate_download(
                "http://127.0.0.1:8000/results/format1/",
                details
            );
            break;
        case 2:
            Initiate_download(
                "http://127.0.0.1:8000/results/format2/",
                details
            );
            break;
        case 6:
            break;
        case 7:
            Initiate_download(
                "http://127.0.0.1:8000/results/format7/",
                details
            );
    }
});

function Initiate_download(url, details) {
    document.getElementById("download").textContent = "Downloading...";
    document.getElementById("download").disabled = true;
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(details),
    })
        .then((response) => {
            // Check if the response is successful (status code 200)
            if (response.ok) {
                // Extract filename from Content-Disposition header
                const filename = response.headers
                    .get("Content-Disposition")
                    .split("filename=")[1];

                document.getElementById("download").textContent = "Download";
                document.getElementById("download").disabled = false;
                // Convert response to a blob
                return response.blob().then((blob) => {
                    // Create a link to the blob
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = filename || "download"; // Set default filename if not provided
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                });
            } else {
                // Handle errors
                console.error("Error:", response.statusText);
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
}

// generate form data
let formData = {
    format_type: "",
    format_number: "",
    course: [],
    year: [],
    semester: [],
};

let formDataC = {
    course: "",
    year: "",
};

// courses data
const courses = [
    "BCA - Morning",
    "BCA - Evening",
    "B.Com H - Morning",
    "B.Com H - Evening",
    "BBA B&I - Morning",
    "BBA B&I - Evening",
    "BBA G - Morning",
    "BBA G - Evening",
    "BBA LLB",
    "BA LLB",
    "B.Ed",
    "MBA",
];
const customCourseSelect = document.getElementById("custom-course-select");
const customCourseSelectC = document.getElementById("custom-course-selectC");
courses.forEach((course) => {
    const option = document.createElement("option");
    option.value = course;
    option.textContent = course;
    customCourseSelect.appendChild(option);
    customCourseSelectC.appendChild(option.cloneNode(true));
});

// custom semester select
const semesterByCourse = {
    "BCA - Morning": 6,
    "BCA - Evening": 6,
    "B.Com H - Morning": 6,
    "B.Com H - Evening": 6,
    "BBA B&I - Morning": 6,
    "BBA B&I - Evening": 6,
    "BBA G - Morning": 6,
    "BBA G - Evening": 6,
    "BBA LLB": 10,
    "BA LLB": 10,
    "B.Ed": 4,
    MBA: 4,
};
const customSemesterSelect = document.getElementById("custom-semester-select");
function addSemesterOptions(selectedCourseOption) {
    if (selectedCourseOption in semesterByCourse) {
        customSemesterSelect.innerHTML = "";
        for (let i = 1; i <= semesterByCourse[selectedCourseOption]; i++) {
            const option = document.createElement("option");
            option.value = `Semester ${i}`;
            option.textContent = `Semester ${i}`;
            customSemesterSelect.appendChild(option);
        }
    }
}
const observerForCourse = new MutationObserver((mutations) => {
    for (let i = 2; i <= step5.children.length; i++) {
        step5.children[i].remove();
    }
    new CustomSelect(customSemesterSelect);
});
observerForCourse.observe(customSemesterSelect, {
    childList: true,
});

// custom-year-select
const customYearSelect = document.getElementById("custom-year-select");
const customYearSelectC = document.getElementById("custom-year-selectC");
function addYearOptions(courseName, id) {
    if (!courses.includes(String(courseName))) return;
    const currentYear = new Date().getFullYear();
    let yearDiff = 0;
    if (id === "custom-course-selectC") {
        customYearSelectC.innerHTML = "";
        yearDiff = semesterByCourse[formDataC.course] / 2;
        for (let i = 0; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear + yearDiff - i;
            option.textContent = `${currentYear - i} - ${
                currentYear + yearDiff - i
            }`;
            customYearSelectC.appendChild(option);
        }
        for (let i = 1; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear - i;
            option.textContent = `${currentYear - yearDiff - i} - ${
                currentYear - i
            }`;
            customYearSelectC.appendChild(option);
        }
    } else {
        customYearSelect.innerHTML = "";
        yearDiff = semesterByCourse[formData.course[entryNumber - 1]] / 2;
        for (let i = 0; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear + yearDiff - i;
            option.textContent = `${currentYear - i} - ${
                currentYear + yearDiff - i
            }`;
            customYearSelect.appendChild(option);
        }
        for (let i = 1; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear - i;
            option.textContent = `${currentYear - yearDiff - i} - ${
                currentYear - i
            }`;
            customYearSelect.appendChild(option);
        }
    }
}
// for generate
const observerForYear = new MutationObserver((mutations) => {
    for (let i = 2; i <= step4.children.length; i++) {
        step4.children[i].remove();
    }
    new CustomSelect(customYearSelect);
});
observerForYear.observe(customYearSelect, { childList: true });

// for configure
const observerForYearC = new MutationObserver((mutations) => {
    for (let i = 2; i <= step2C.children.length; i++) {
        step2C.children[i].remove();
    }
    new CustomSelect(customYearSelectC);
});
observerForYearC.observe(customYearSelectC, { childList: true });

// custom format select
let formatByFormatType = {
    Faculty: [1, 6],
    Management: [2, 7],
};
const customFormatSelect = document.getElementById("custom-format-select");
function handleFormatTypeChange() {
    console.log("changed");
}
function addFormatOptions(selectedFormatTypeOption) {
    if (
        !(
            String(selectedFormatTypeOption) === "Faculty" ||
            String(selectedFormatTypeOption) === "Management"
        )
    )
        return;
    customFormatSelect.innerHTML = "";

    for (
        let i = 0;
        i < formatByFormatType[selectedFormatTypeOption].length;
        i++
    ) {
        const option = document.createElement("option");
        option.value = formatByFormatType[selectedFormatTypeOption][i];
        option.textContent = `Format ${formatByFormatType[selectedFormatTypeOption][i]}`;
        customFormatSelect.appendChild(option);
    }
}
const observerForFormatType = new MutationObserver((mutations) => {
    if (formData.format_number !== "") return;

    for (let i = 2; i <= step2.children.length; i++) {
        step2.children[i].remove();
    }
    new CustomSelect(customFormatSelect);
});

observerForFormatType.observe(customFormatSelect, {
    childList: true,
});

// modal close btn
const modalCloseBtn = document.getElementById("modal_close");
modalCloseBtn.addEventListener("click", () => {
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
    modal.children[1].innerHTML = "";
});

//  custom select
class CustomSelect {
    constructor(originalSelect) {
        this.originalSelect = originalSelect;
        this.customSelect = document.createElement("div");
        this.customSelect.classList.add("select");

        this.originalSelect
            .querySelectorAll("option")
            .forEach((optionElement) => {
                const itemElement = document.createElement("div");
                itemElement.classList.add("select__item");
                itemElement.textContent = optionElement.textContent;
                if (originalSelect.id === "custom-format-select") {
                    itemElement.classList.add("flex");
                    itemElement.classList.add("justify-between");
                    itemElement.classList.add("items-center");
                    itemElement.textContent = `Format ${optionElement.value}`;
                    const imgElement = document.createElement("img");
                    imgElement.src = `/static/preview.svg`;

                    itemElement.appendChild(imgElement);

                    imgElement.addEventListener("click", (event) => {
                        event.stopPropagation();
                        const modal = document.getElementById("modal");
                        modal.classList.remove("hidden");
                        const img = document.createElement("img");
                        img.src = `/static/Format${optionElement.value}.png`;
                        img.alt = `Format ${optionElement.value}`;
                        modal.children[1].appendChild(img);
                    });
                }

                this.customSelect.appendChild(itemElement);

                itemElement.addEventListener("click", () => {
                    if (
                        itemElement.classList.contains("select__item--selected")
                    ) {
                        this._deselect(itemElement);
                    } else {
                        this._select(itemElement);
                    }
                });
            });

        this.originalSelect.insertAdjacentElement(
            "afterend",
            this.customSelect
        );
        this.originalSelect.style.display = "none";
    }

    _select(itemElement) {
        const index = Array.from(this.customSelect.children).indexOf(
            itemElement
        );

        this.customSelect.querySelectorAll(".select__item").forEach((el) => {
            el.classList.remove("select__item--selected");
        });

        this.originalSelect.querySelectorAll("option")[index].selected = true;
        let value = this.originalSelect.querySelectorAll("option")[index].value;

        if (this.originalSelect.id[this.originalSelect.id.length - 1] === "C")
            this._setFormDataC(value);
        else this._setFormData(value);
        itemElement.classList.add("select__item--selected");
        document.getElementById("selected").innerHTML = `Selected: ${value}`;
        addSemesterOptions(itemElement.textContent);
        addYearOptions(itemElement.textContent, this.originalSelect.id);
        addFormatOptions(itemElement.textContent);
    }

    _setFormData(value) {
        if (currentStep <= 2) {
            formData[Object.keys(formData)[currentStep - 1]] = value;
        } else {
            formData[Object.keys(formData)[currentStep - 1]][entryNumber - 1] =
                value;
        }
        console.log(formData);
    }

    _setFormDataC(value) {
        formDataC[Object.keys(formDataC)[currentStepC - 1]] = value;
        console.log(formDataC);
    }

    _deselect(itemElement) {
        const index = Array.from(this.customSelect.children).indexOf(
            itemElement
        );

        this.originalSelect.querySelectorAll("option")[index].selected = false;
        itemElement.classList.remove("select__item--selected");
    }
}

document.querySelectorAll(".custom-select").forEach((selectElement) => {
    new CustomSelect(selectElement);
});

// configure form
//            btn = document.getElementById("btn");
//           btn.addEventListener("click", function (event) {
//              event.preventDefault();
//             form = document.getElementById("pdfForm");
//            const formData = new FormData(form);
//           console.log(formData);

//          fetch("http://127.0.0.1:8000/results/normalize/", {
//             method: "POST",
//            body: formData,
//       })
//          .then((response) => response.blob())
//                         .then((blob) => {
//                            console.log(blob);
//                           const url = window.URL.createObjectURL(blob);
//                          const a = document.createElement("a");
//                         a.href = url;
//                        a.download = "normalized.xlsx";
//                       a.textContent = "Download Normalized excel file";
//                      document.getElementById("result").appendChild(a);
//                 })
//                .catch((error) => {
//                   console.error("Fetch Error:", error);
//              });
//     });
