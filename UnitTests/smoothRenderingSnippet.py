# Nuke's solution for smooth rendering: test this later with openai
# for chunk in self.master.storyGenObj: #type: ignore
#     if any(chunk.endswith(char) for char in ['.', '?', '!']):
#         punct_marks = ['.', '?', '!']
#         for mark in punct_marks:
#             if chunk.endswith(f'{mark}'):
#                 self.chatBox.insert('end', f"{mark}\n")
#         time.sleep(0.03)
#     else:
#         self.chatBox.insert('end', chunk)
#         time.sleep(0.03)