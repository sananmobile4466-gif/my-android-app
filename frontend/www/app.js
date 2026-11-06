// Change this to your backend's reachable address when deploying or using on a phone.
const API_BASE = "http://localhost:8000";
const $ = id => document.getElementById(id);
let selected = null;
$("video").addEventListener("change", e => {
  selected = e.target.files[0] || null;
  $("filename").textContent = selected ? `${selected.name} · ${(selected.size/1024/1024).toFixed(1)} MB` : "No video selected";
});
$("go").addEventListener("click", async () => {
  if (!selected) { $("status").textContent = "Please choose a video first."; return; }
  const btn = $("go"); btn.disabled = true; $("status").textContent = "Uploading and processing…";
  $("results").classList.add("hidden");
  const data = new FormData();
  data.append("video", selected);
  data.append("clip_seconds", $("duration").value);
  data.append("vertical", $("format").value === "vertical" ? "true" : "false");
  data.append("smart_highlights", $("smart").checked ? "true" : "false");
  try {
    const response = await fetch(`${API_BASE}/process`, {method:"POST", body:data});
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Processing failed");
    $("cliplist").innerHTML = "";
    result.clips.forEach((clip, i) => {
      const url = API_BASE + clip.url;
      const row = document.createElement("article"); row.className = "clip";
      const info = document.createElement("div");
      const title = document.createElement("strong"); title.textContent = `Clip ${i+1} · ${formatTime(clip.start)} – ${formatTime(clip.start+clip.duration)}`;
      const meta = document.createElement("div"); meta.className = "tag";
      meta.textContent = clip.score == null ? `${Math.round(clip.duration)} sec` : `Smart score: ${clip.score}`;
      info.append(title, meta);
      const link = document.createElement("a"); link.className = "download"; link.href = url; link.download = clip.name; link.textContent = "Download";
      const player = document.createElement("video"); player.controls = true; player.preload = "metadata"; player.src = url;
      row.append(info, link, player); $("cliplist").append(row);
    });
    $("results").classList.remove("hidden");
    $("status").textContent = `Done — ${result.clip_count} clips created.`;
  } catch (err) { $("status").textContent = `Error: ${err.message}. Check that the backend is running and API_BASE is correct.`; }
  finally { btn.disabled = false; }
});
function formatTime(s){const m=Math.floor(s/60), sec=Math.floor(s%60);return `${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;}
