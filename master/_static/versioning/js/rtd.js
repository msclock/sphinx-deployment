/**
 * Handles the click event.
 *
 * @param {Event} event - The click event object.
 * @return {undefined} This function does not return a value.
 */
function handleClick(event) {
  if (event.currentTarget.classList.contains("shift-up"))
    event.currentTarget.classList.remove("shift-up");
  else event.currentTarget.classList.add("shift-up");
}

/**
 * Locates the URL of the versions.json file by recursively checking parent directories.
 *
 * @param {string} url - The URL of the current directory.
 * @return {string} The URL of the versions.json file, or null if not found.
 */
async function locateVersionsJsonUrl(url) {
  let checkUrl = url.endsWith("/") ? url.slice(0, -1) : url;
  let response;

  while (checkUrl !== "") {
    try {
      response = await fetch(checkUrl + "/versions.json");
      if (response.ok) {
        return checkUrl + "/versions.json";
      }
    } catch (error) {
      console.warn("Failed to find versions.json at " + checkUrl + ":", error);
    }

    checkUrl = checkUrl.substring(0, checkUrl.lastIndexOf("/"));
  }

  return null;
}

window.addEventListener("DOMContentLoaded", async function () {
  try {
    var versionsJsonUrl = await locateVersionsJsonUrl(
      this.window.location.href.substring(
        0,
        this.window.location.href.lastIndexOf("/"),
      ),
    );
  } catch (error) {
    console.error("Failed to find versions.json");
  }
  if (versionsJsonUrl === null) {
    console.error("Failed to find versions.json");
    return;
  }
  var rootUrl = versionsJsonUrl.slice(0, versionsJsonUrl.lastIndexOf("/"));
  var currentVersionPath = this.window.location.href.substring(rootUrl.length);
  var currentVersion = currentVersionPath.match(/\/([^\/]+)\//)[1];

  const response = await fetch(versionsJsonUrl);
  if (!response.ok) {
    throw new Error("Failed to fetch versions.json");
  }
  const versionsJson = await response.json();

  if (!(currentVersion in versionsJson.versions)) {
    console.error("Current version not found in versions.json");
    return;
  }

  // Create injected div
  var injectedDiv = document.createElement("div");
  injectedDiv.setAttribute("id", "injected");
  document.body.appendChild(injectedDiv);

  // Add style
  const link1 = document.createElement("link");
  link1.setAttribute("rel", "stylesheet");
  link1.setAttribute(
    "href",
    "https://www.w3schools.cn/cdnjs/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
  );
  injectedDiv.appendChild(link1);

  // Create and append the rstVersionsDiv
  const rstVersionsDiv = document.createElement("div");
  rstVersionsDiv.setAttribute("class", "rst-versions rst-badge");
  rstVersionsDiv.addEventListener("click", handleClick);
  injectedDiv.appendChild(rstVersionsDiv);

  // Current version
  const rstCurrentVersionSpan = document.createElement("span");
  rstCurrentVersionSpan.setAttribute("class", "rst-current-version");
  rstVersionsDiv.appendChild(rstCurrentVersionSpan);

  // Append a book icon
  const bookIconSpan = document.createElement("span");
  bookIconSpan.setAttribute("class", "fa fa-book");
  bookIconSpan.appendChild(document.createTextNode("\u00A0"));
  rstCurrentVersionSpan.appendChild(bookIconSpan);

  // Add a space
  rstCurrentVersionSpan.appendChild(document.createTextNode("\u00A0"));

  // Current version
  const versionText = document.createTextNode(currentVersion);
  rstCurrentVersionSpan.appendChild(versionText);

  // Add a space
  rstCurrentVersionSpan.appendChild(document.createTextNode("\u00A0"));

  // Append a caret icon
  const caretSpan = document.createElement("span");
  caretSpan.setAttribute("class", "fa fa-caret-down");
  rstCurrentVersionSpan.appendChild(caretSpan);

  // Other versions
  const rstOtherVersionsDiv = document.createElement("div");
  rstOtherVersionsDiv.setAttribute("class", "rst-other-versions");
  rstVersionsDiv.appendChild(rstOtherVersionsDiv);

  // Append a dl element in rstOtherVersionsDiv
  const dl = document.createElement("dl");
  rstOtherVersionsDiv.appendChild(dl);

  // Append a dt element in dl
  const dt = document.createElement("dt");
  dt.appendChild(document.createTextNode("Versions"));
  dl.appendChild(dt);

  // Iterate over versions and append dd elements to dl
  Object.entries(versionsJson.versions).forEach(([_, ver]) => {
    const dd = document.createElement("dd");
    dd.setAttribute("class", "rtd-current-item");
    const link = document.createElement("a");
    link.setAttribute("href", rootUrl + "/" + ver.name + "/");
    link.appendChild(document.createTextNode(ver.name));
    dd.appendChild(link);
    dl.appendChild(dd);
  });

  // Append an hr element as a separator
  rstOtherVersionsDiv.appendChild(document.createElement("hr"));

  // Append a small element
  const small = document.createElement("small");
  rstOtherVersionsDiv.appendChild(small);

  // Generator info
  const generatorSpan = document.createElement("span");
  small.appendChild(generatorSpan);
  generatorSpan.appendChild(document.createTextNode("Generated by "));
  const generatorLink = document.createElement("a");
  generatorSpan.appendChild(generatorLink);
  generatorLink.setAttribute(
    "href",
    "https://github.com/msclock/sphinx-deployment",
  );
  generatorLink.appendChild(document.createTextNode("sphinx-deployment"));
});
