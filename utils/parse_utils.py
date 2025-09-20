def parse_added_bullets_from_generated(generated_text):
    added, uid = [], 0
    for line in generated_text.splitlines():
        if line.strip().startswith("- [ADDED_FROM_JD]"):
            plain = line.strip()[len("- [ADDED_FROM_JD]"):].strip()
            added.append({"id": f"added_{uid}", "line": line, "bullet_text": plain})
            uid += 1
    return added

def remove_or_replace_added_bullets(generated_text, edits_map):
    lines, out_lines, added_idx = generated_text.splitlines(), [], 0
    for line in lines:
        if line.strip().startswith("- [ADDED_FROM_JD]"):
            key = f"added_{added_idx}"
            info = edits_map.get(key, {"keep": True, "text": None})
            if info["keep"]:
                new_text = info.get("text") or line.strip()[len("- [ADDED_FROM_JD]"):].strip()
                out_lines.append("- " + new_text)
            added_idx += 1
        else:
            out_lines.append(line)
    return "\n".join(out_lines).replace("[ADDED_FROM_JD]", "").replace("  ", " ")
