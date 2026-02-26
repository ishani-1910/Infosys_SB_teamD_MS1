import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------------------------------
# 🔧 CONFIGURATION
# -------------------------------------------------------------------------
# PASTE YOUR AGENT X CODE INSIDE THE TRIPLE QUOTES BELOW.
# It should look like: <script ...> ... </script>
AGENT_CODE_SNIPPET = """
<div id="chatInlineRoot-b32611">
  <script defer src="https://storage.googleapis.com/agentx-cdn-01/agentx-chat.js?agx=6980a939a5dca7877db32611DDOeSTyo4L%2FWrQGyflMUpQ%3D%3D%7ChpTnpxQWRA6GGgEtGc%2FGrtQVoNqvzZtZtH6Wx6Azg9w%3D"></script>
  </div>

<h3 style="text-align:center; color:#666;">Agent X Widget Will Load Here</h3>
<p style="text-align:center;">(Paste your script in <code>agent_interface.py</code>)</p>

"""

def show_agent_page():
    """
    Renders the Agent X script inside a Streamlit container.
    """
    st.markdown("<h2 class='section-title'>AI Companion</h2>", unsafe_allow_html=True)
    st.markdown("I'm here to listen. This is a safe space to chat.")

    # Render the Javascript/HTML snippet
    # We set a high height (800px) to ensure the chat window has space.
    # scrolling=True allows the user to scroll if the chat gets long.
    components.html(AGENT_CODE_SNIPPET, height=800, scrolling=True)