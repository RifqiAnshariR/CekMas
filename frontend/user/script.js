import stringSimilarity from 'https://cdn.jsdelivr.net/npm/string-similarity/+esm';

document.getElementById("startBtn").addEventListener("click", () => goToPage("page2"));
document.getElementById("statusBtn").addEventListener("click", () => goToPage("statusPage"));
document.getElementById("submitTicketBtn").addEventListener("click", checkStatus);
document.getElementById("submitImageBtn").addEventListener("click", submitImage);
document.getElementById("submitDataBtn").addEventListener("click", submitData);
document.getElementById("sendMessageBtn").addEventListener("click", sendMessage);

function goToPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('visible'));
    document.getElementById(pageId).classList.add('visible');
}

async function checkStatus() {
    const ticket = document.getElementById("ticket").value.trim();
    const resultDiv = document.getElementById("statusResult");

    if (!ticket) {
        alert("Masukkan nomor tiket terlebih dahulu.");
        return;
    }

    try {
        const res = await fetch(`http://127.0.0.1:8000/status/${ticket}`, {
            method: "GET"
        });
        const data = await res.json();
        if (data.status) {
            resultDiv.innerHTML = `
                <br>
                <div class="status-result">
                    <p><b>Email:</b> ${data.email}</p>
                    <p><b>NIK:</b> ${data.nik}</p>
                    <p><b>Nama:</b> ${data.name}</p>
                    <p><b>Status:</b> ${data.status}</p>
                </div>
                <br><br>
            `;
        } else {
            alert("Laporan tidak ditemukan.");
        }
    } catch (err) {
        alert("Error: " + err + ". Tolong refresh browser anda.");
    }
}

async function submitImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    if (!file) {
        alert("Upload gambar terlebih dahulu!");
        return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    try {
        const res = await fetch("http://127.0.0.1:8000/upload_ktp", {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        document.getElementById("nik").value = data.nik;
        document.getElementById("name").value = data.nama;
        if (data.gender === "LAKI LAKI") {
            document.getElementById("laki").checked = true;
        } else {
            document.getElementById("perempuan").checked = true;
        }

        goToPage("page3");

    } catch (err) {
        alert("Error: " + err + ". Tolong refresh browser anda.");
    }
}

async function submitData() {
    const email = document.getElementById('email').value;
    const nik = document.getElementById('nik').value;
    const name = document.getElementById('name').value;
    const gender = document.querySelector('input[name="gender"]:checked')?.value;

    if (!email || !nik || !name || !gender) {
        alert("Isi semua data!");
        return;
    }

    sessionStorage.setItem("email", email);
    sessionStorage.setItem("nik", nik);
    sessionStorage.setItem("name", name);
    sessionStorage.setItem("gender", gender);
    sessionStorage.setItem("chatState", 0);

    goToPage("page4");
}

async function saveReport(email, nik, name, location, message, category, sentiment) {
    try {
        const res = await fetch("http://127.0.0.1:8000/save_report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email,
                nik: nik,
                name: name,
                location: location,
                message: message,
                category: category,
                sentiment: sentiment
            })
        });
        const data = await res.json();
        return data.ticket;
    } catch (err) {
        alert("Error: " + err + ". Tolong refresh browser anda.");
    }
}

function addMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const div = document.createElement("div");
    div.className = "bubble " + className;
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addImageMessage(className) {
    const chatBox = document.getElementById("chatBox");
    const div = document.createElement("div");
    div.className = "bubble " + className;

    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";

    const button = document.createElement("button");
    button.textContent = "Submit";

    button.onclick = async () => {
        const file = input.files[0];
        if (!file) {
            alert("Upload gambar terlebih dahulu!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch("http://127.0.0.1:8000/upload_bukti", {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            getResponse(4, "")
        } catch (err) {
            addMessage("Error: " + err + ". Tolong refresh browser anda.", "botBubble");
        }
    };

    div.appendChild(input);
    div.appendChild(button);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("chatInput");
    const message = input.value;
    if (!message) return;

    addMessage(message, "userBubble");
    input.value = "";

    let state = Number(sessionStorage.getItem("chatState"));

    if (state === 1) {
        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });
            const data = await res.json();
            sessionStorage.setItem("category", data.category)
            sessionStorage.setItem("sentiment", data.sentiment)
            sessionStorage.setItem("response", data.response)
            sessionStorage.setItem("follow_up_1", data.follow_up_1)
            sessionStorage.setItem("follow_up_2", data.follow_up_2)
        } catch (err) {
            addMessage("Error: " + err +". Tolong refresh browser anda.", "botBubble");
            return;
        }
    }

    return getResponse(state, message)
}

function getResponse(state, message) {
    const email = sessionStorage.getItem("email");
    const nik = sessionStorage.getItem("nik");
    const name = sessionStorage.getItem("name");
    const gender = sessionStorage.getItem("gender");
    const category = sessionStorage.getItem("category");
    const sentiment = sessionStorage.getItem("sentiment");
    const response = sessionStorage.getItem("response");
    const follow_up_1 = sessionStorage.getItem("follow_up_1");
    const follow_up_2 = sessionStorage.getItem("follow_up_2");
    const message_1 = sessionStorage.getItem("message_1") || "";
    const message_2 = sessionStorage.getItem("message_2") || "";
    const message_3 = sessionStorage.getItem("message_3") || "";

    if (state === 0) {
        const pronoun = (gender === "LAKI LAKI") ? "Pak" : "Bu";
        addMessage(`Halo ${pronoun} ${name}. Selamat datang di layanan CekMas. Boleh dijelaskan hal yang ingin dilaporkan?`, "botBubble");
        sessionStorage.setItem("chatState", ++state);
    }

    else if (state === 1) {
        addMessage(response, "botBubble");
        addMessage(follow_up_1, "botBubble");
        sessionStorage.setItem("message_1", message);
        sessionStorage.setItem("chatState", ++state);
    }

    else if (state === 2) {
        addMessage(follow_up_2, "botBubble");
        sessionStorage.setItem("message_2", message);
        sessionStorage.setItem("chatState", ++state);
    }

    else if (state === 3) {
        addMessage("Upload bukti apabila ada. Jika tidak ada balas 'tidak'.", "botBubble");
        addImageMessage("uploadBubble")
        sessionStorage.setItem("message_3", message);
        sessionStorage.setItem("chatState", ++state);
    }

    else if (state === 4) {
        const location = message_2;
        const full_message = message_1 + ", " + message_3;
        saveReport(email, nik, name, location, full_message, category, sentiment)
            .then(ticket_id => {
                addMessage(`Pesan sudah disimpan. Berikut nomer tiket anda: ${ticket_id}`, "botBubble");
                addMessage("Apakah ada hal lain yang ingin disampaikan? Ini akan membuat sesi laporan baru.", "botBubble");
                sessionStorage.setItem("chatState", ++state);
            });
    }

    else if (state === 5) {
        const keyword = ['tidak', 'enggak', 'keluar', 'exit', 'no']
        if (stringSimilarity.findBestMatch(message.toLowerCase(), keyword).bestMatch.rating > 0.7) {
            goToPage("page5");
        } else {
            addMessage("Boleh dijelaskan hal yang ingin disampaikan?", "botBubble");
            sessionStorage.setItem("chatState", 1);
        }
    }
}
