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
function previewDivDetails() {
    const previewHeader = document.getElementById("previewHeader");
    updatePreviewBody();
    previewHeader.innerHTML = "";
    if (
        formData.course.length < 1 &&
        formData.semester.length < 1 &&
        formData.year.length < 1
    ) {
        alert("Please fill all the fields");
        return;
    }

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
        for (let j = 2; j < 5; j++) {
            const p = document.createElement("p");
            p.classList.add("text-lg");
            p.textContent = formData[Object.keys(formData)[j]][i];
            div.appendChild(p);
        }
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
        div.setAttribute("id", `entryHeader${i + 1}`);
        cancelImg.setAttribute("id", `cancel${i + 1}`);
        div.addEventListener("click", () => {
            entrySelected = div.id[div.id.length - 1];
            updateEntry();
            for (let i = 1; i <= entryNumber; i++) {
                const entry = document.getElementById(`entry${i}`);
                entry.classList.add("hidden");
                if (i == entrySelected) {
                    entry.classList.remove("hidden");
                }
            }
        });
        previewHeader.appendChild(div);
    }
    updateEntry();
    for (let i = 1; i <= entryNumber; i++) {
        const entry = document.getElementById(`entry${i}`);
        entry.classList.add("hidden");
        if (i == entrySelected) {
            entry.classList.remove("hidden");
        }
    }
}
function updateEntry() {
    for (let i = 1; i <= entryNumber; i++) {
        const entry = document.getElementById(`entryHeader${i}`);
        entry.classList.remove("bg-primaryPurple");
        entry.classList.add("bg-gray2");
        if (i == entrySelected) {
            entry.classList.remove("bg-gray2");
            entry.classList.add("bg-primaryPurple");
        }
    }
}

function updatePreviewBody() {
    const previewBody = document.getElementById("previewBody");
    previewBody.innerHTML = "";
    const div = document.createElement("div");
    switch (Number(formData.format_number)) {
        case 1:
            div.setAttribute("id", "format1");
            for (let i = 0; i < entryNumber; i++) {
                const entryDiv = document.createElement("div");
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
                const subjectCodes = document.createElement("input");
                subjectCodes.classList.add(
                    "border",
                    "border-gray",
                    "p-2",
                    "rounded-md"
                );
                subjectCodes.setAttribute("type", "text");
                subjectCodes.setAttribute("placeholder", "Subject Codes");
                subjectCodes.setAttribute("name", "subject_codes");
                entryDiv.appendChild(name);
                entryDiv.appendChild(section);
                entryDiv.appendChild(subjectCodes);
                div.appendChild(entryDiv);
            }
            break;
        case 2:
            div.setAttribute("id", "format2");
            div.innerHTML = "format2";
            break;
        case 6:
            div.setAttribute("id", "format6");
            div.innerHTML = "format6";
            break;
        case 7:
            div.setAttribute("id", "format7");
            div.innerHTML = "format7";
            break;
    }
    previewBody.appendChild(div);
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
next.addEventListener("click", function () {
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
            previewDivDetails();
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

    // handle generate
    let shift = [];
    for (let i = 0; i < formData.course.length; i++) {
        shift.push(formData.course[i].split(" ").pop() != "Morning" ? 2 : 1);
    }
    //checking if all the courses are of same shift
    if (!shift.every((val) => val === shift[0])) {
        alert("Please select same shift for all the courses");
        return;
    }
    details.course = formData.course.map((str) => str.split(" ")[0]);
    details.shift = shift[0];
    details.semester = formData.semester.map((str) => str.slice(-1));
    details.passing = formData.year;

    let faculty_name = [],
        sections = [],
        subjectcodes = [],
        subjectCodesPerEntry = [];
    for (let i = 0; i < entryNumber; i++) {
        const entry = document.getElementById(`entry${i + 1}`);
        faculty_name.push(entry.children[0].value);
        sections.push(String(entry.children[1].value).toUpperCase());
        subjectcodes.push(
            ...entry.children[2].value.split(",").map((str) => str.trim())
        );
        subjectCodesPerEntry.push(entry.children[2].value.split(" ").length);
    }
    if (!faculty_name.every((val) => val === faculty_name[0])) {
        alert("Please select same faculty for all the entries");
        return;
    }

    details.faculty_name = faculty_name[0];
    details.sections = sections;
    details.subjectcodes = subjectcodes;

    // transforming the details object
    // minimum number of times the values repeat is the number of entries and maximum is the number of subjects in a semester
    let course = [],
        passing = [],
        semester = [],
        sectionsTransformed = [];
    // assuming that there will be atleast one subject code for each entry.
    subjectCodesPerEntry.forEach((val, index) => {
        for (let i = 0; i < val; i++) {
            course.push(details.course[index]);
            passing.push(details.passing[index]);
            semester.push(details.semester[index]);
            sectionsTransformed.push(details.sections[index]);
        }
    });
    details.course = course;
    details.passing = passing;
    details.semester = semester;
    details.sections = sectionsTransformed;
    details.indices = subjectCodesPerEntry;

    console.log("download", details);
    generate.classList.add("hidden");
    download.classList.remove("hidden");
});

download.addEventListener("click", function () {
    // handle download
    fetch("http://127.0.0.1:8000/results/format1/", {
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
});

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
            option.textContent = `${currentYear - i} - ${currentYear + yearDiff - i}`
            customYearSelectC.appendChild(option);
        }
        for (let i = 1; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear - i;
            option.textContent = `${currentYear - yearDiff - i} - ${currentYear - i}`
            customYearSelectC.appendChild(option);
        }
    } else {
        customYearSelect.innerHTML = "";
        yearDiff = semesterByCourse[formData.course[entryNumber - 1]] / 2;
        for (let i = 0; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear + yearDiff - i;
            option.textContent = `${currentYear - i} - ${currentYear + yearDiff - i}`
            customYearSelect.appendChild(option);
        }
        for (let i = 1; i <= yearDiff; i++) {
            const option = document.createElement("option");
            option.value = currentYear - i;
            option.textContent = `${currentYear - yearDiff - i} - ${currentYear - i}`
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
