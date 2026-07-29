const rebuildStatusElement = document.getElementById("rebuild-status");
const refreshButton = document.getElementById("refresh-status");
const triggerRebuildButton = document.getElementById("trigger-rebuild");
const userIdInput = document.getElementById("user-id");
const sessionIdInput = document.getElementById("session-id");
const chatMessages = document.getElementById("chat-messages");
const errorBanner = document.getElementById("error-banner");
const chatForm = document.getElementById("chat-form");
const userMessageInput = document.getElementById("user-message");
const sendButton = document.getElementById("send-button");

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove("hidden");
}

function hideError() {
  errorBanner.textContent = "";
  errorBanner.classList.add("hidden");
}

function addChatMessage(role, content) {
  const wrapper = document.createElement("div");
  wrapper.className = `chat-message ${role}`;

  const roleLabel = document.createElement("div");
  roleLabel.className = "message-role";
  roleLabel.textContent = role;

  const text = document.createElement("div");
  text.className = "message-content";
  text.textContent = content;

  wrapper.appendChild(roleLabel);
  wrapper.appendChild(text);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function updateHealth() {
  try {
    const response = await fetch("/api/health");
    if (!response.ok) throw new Error("Health request failed.");
    const payload = await response.json();
    rebuildStatusElement.textContent = payload.rebuild?.status ?? "unknown";
  } catch (err) {
    rebuildStatusElement.textContent = "unavailable";
  }
}

async function triggerRebuild() {
  hideError();
  try {
    const response = await fetch("/api/rebuild", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clear_graph: false }),
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Rebuild failed: ${response.status} ${errorText}`);
    }
    const payload = await response.json();
    rebuildStatusElement.textContent = payload.status ?? "unknown";
  } catch (err) {
    showError(err instanceof Error ? err.message : "Could not trigger rebuild.");
  }
}

async function sendMessage(event) {
  event.preventDefault();
  hideError();

  const message = userMessageInput.value.trim();
  if (!message) return;

  sendButton.disabled = true;
  addChatMessage("user", message);
  userMessageInput.value = "";

  const payload = {
    user_id: userIdInput.value.trim() || "demo-user",
    message,
  };

  if (sessionIdInput.value.trim()) {
    payload.session_id = sessionIdInput.value.trim();
  }

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Chat failed: ${response.status} ${errorText}`);
    }
    const data = await response.json();
    sessionIdInput.value = data.session_id ?? sessionIdInput.value;
    addChatMessage("assistant", data.response ?? "No response from the server.");
  } catch (err) {
    addChatMessage("assistant", "I could not send your message. Please try again later.");
    showError(err instanceof Error ? err.message : "Unable to send chat message.");
  } finally {
    sendButton.disabled = false;
  }
}

refreshButton.addEventListener("click", updateHealth);
triggerRebuildButton.addEventListener("click", triggerRebuild);
chatForm.addEventListener("submit", sendMessage);

updateHealth();
