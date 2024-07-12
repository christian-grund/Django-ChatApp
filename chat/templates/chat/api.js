const URLTEST = "https//test123.de";
const data = {
	title: "foo",
	body: "bar",
	userID: 1,
};

// GET
async function fetchData() {
	try {
		let response = await fetch(URLTEST);
		if (!response.ok) {
			console.error(`HTTP-Error! Status: ${response.status}`);
		}
		let responseAsJson = await response.json();
		console.log(responseAsJson);
	} catch (error) {
		console.error("Es gab ein Problem mit der Fetch-Operation:", error);
	}
}

// POST
async function postData() {
	const url = "https://jsonplaceholder.typicode.com/posts";

	try {
		let response = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});
		let responseAsJson = await response.json();
		console.log(responseAsJson);

		// Rufe die Funktion auf, um die erstellte Ressource zu aktualisieren
		putData(responseAsJson.id);
	} catch (error) {
		console.error("Es gab ein Problem mit der Fetch-Operation:", error);
	}
}

// PUT
async function putData(postId) {
	const url = `https://jsonplaceholder.typicode.com/posts/${postId}`;
	const updatedData = {
		id: postId,
		title: "updatedTitle",
		body: "updatedBody",
		userID: 2,
	};

	try {
		let response = await fetch(URLTEST, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(updatedData),
		});

		if (!response.ok) {
			throw new Error(`HTTP-Fehler! Status: ${response.status}`);
		}

		let putResponseAsJson = await response.json();
		console.log("PUT Response:", putResponseAsJson);
	} catch (error) {
		console.error("Es gab ein Problem mit der Fetch-Operation:", error);
	}
}

// PATCH
async function patchData() {
	const patchData = {
		body: "patchedBody",
	};
	try {
		let response = await fetch("https://jsonplaceholder.typicode.com/posts/1", {
			method: "PATCH",
			headers: {
				// headers statt head!
				"Content-Type": "application/json",
			},
			body: JSON.stringify(patchData), // kein Semikolon!
		});

		if (!response.ok) {
			console.error(`An error occured: ${response.status}`);
		}

		patchResponseAsJson = await response.json();
		console.log("PATCH Response:", patchResponseAsJson);

		// Rufe die Funktion auf, um die erstellte Ressource zu löschen
		deleteData(patchResponseAsJson.id);
	} catch (error) {
		console.error(`An error occured: ${error}`);
	}
}

// DELETE
async function deleteData(patchId) {
	const url = `https://jsonplaceholder.typicode.com/posts/${patchId}`;
	try {
		let response = await fetch(url, {
			method: "DELETE",
		});

		if (!response.ok) {
			console.error(`An error occured: ${response.status}`);
		}

		console.log("DELETE Response: The ressource has been deleted succesfully.");
	} catch (error) {
		console.error(`An error occured: ${error}`);
	}
}
