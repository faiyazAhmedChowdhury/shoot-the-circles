
<body>
    <h1>🚀 Shoot The Circles! - A 2D Shooting Game</h1>

  <h2>🎯 Project Overview</h2>
    <p>"Shoot The Circles!" is a <strong>2D shooting game</strong> built using <strong>OpenGL and GLUT</strong>. The game demonstrates <strong>Midpoint Line</strong> and <strong>Midpoint Circle Algorithms</strong> to render all game elements using <code>GL_POINTS</code>.</p>

  <h2>🔖 Game Description</h2>
    <ul>
        <li>The player controls a <strong>spaceship</strong> at the bottom of the screen.</li>
        <li>The spaceship moves <strong>left ('A')</strong> and <strong>right ('D')</strong> within screen limits.</li>
        <li>Pressing <strong>Spacebar</strong> fires a projectile (<strong>circles</strong>) upwards.</li>
        <li><strong>Falling circles</strong> appear at random positions from the top.</li>
        <li>The goal is to <strong>shoot the falling circles</strong> before they reach the ground.</li>
    </ul>

  <h2>🔥 Game Features</h2>
    <ul>
        <li><strong>Midpoint Line Algorithm</strong> for spaceship and projectile rendering.</li>
        <li><strong>Midpoint Circle Algorithm</strong> for falling circles.</li>
        <li><strong>Collision Detection</strong> using Axis-Aligned Bounding Box (AABB).</li>
        <li><strong>Game Over Conditions:</strong>
            <ul>
                <li>A circle touches the spaceship.</li>
                <li>The player misses <strong>three falling circles</strong>.</li>
                <li>The player fires <strong>three consecutive missed shots</strong>.</li>
            </ul>
        </li>
        <li><strong>Score Display</strong> in the console.</li>
        <li><strong>UI Controls:</strong>
            <ul>
                <li><strong>Restart Button</strong> (⬅️) resets the game.</li>
                <li><strong>Pause/Play Button</strong> toggles game state.</li>
                <li><strong>Exit Button</strong> closes the game with a "Goodbye" message.</li>
            </ul>
        </li>
    </ul>

  <h2>🕹️ Controls</h2>
    <table>
        <tr>
            <th>Key/Button</th>
            <th>Action</th>
        </tr>
        <tr><td>A</td><td>Move spaceship left</td></tr>
        <tr><td>D</td><td>Move spaceship right</td></tr>
        <tr><td>Spacebar</td><td>Shoot projectile</td></tr>
        <tr><td>⬅️ Restart</td><td>Reset game</td></tr>
        <tr><td>⏸ Play/Pause</td><td>Pause/Resume game</td></tr>
        <tr><td>❌ Exit</td><td>Quit game</td></tr>
    </table>

  <h2>📺 Installation & Execution</h2>
    <h3>1️⃣ Clone the Repository</h3>
    <pre><code>https://github.com/faiyazAhmedChowdhury/shoot-the-circles</code></pre>

  <h3>2️⃣ Install Dependencies</h3>
    <p>Ensure you have <strong>Python 3.x</strong> installed.</p>
    <pre><code>pip install OpenGL GLUT</code></pre>

  <h3>3️⃣ Run the Game</h3>
    <pre><code>python shoot-the-circles.py</code></pre>

  <h2>🖼️ Screenshots and videos</h2>
    <p>
<img width="600" alt="Screenshot 2025-01-25 at 11 55 11 PM" src="https://github.com/user-attachments/assets/0fb59535-796b-4e2c-9599-49d719e327f2" />

</p>

https://github.com/user-attachments/assets/1208a977-c6fe-4d79-ac43-6f6d11da1833



  <h2>💡 Algorithm Breakdown</h2>
    <h3>1️⃣ Midpoint Line Algorithm</h3>
    <ul>
        <li>Used to draw the spaceship, projectiles, and UI elements.</li>
        <li>Converts all points into <strong>Zone-0</strong> for uniform processing.</li>
        <li>Uses <strong>decision parameters</strong> to select the closest pixel.</li>
    </ul>

  <h3>2️⃣ Midpoint Circle Algorithm</h3>
    <ul>
        <li>Used for rendering both <strong>falling circles</strong> and <strong>projectiles</strong>.</li>
        <li>Leverages <strong>8-way symmetry</strong> for optimized drawing.</li>
        <li>Uses a <strong>decision parameter</strong> to determine the next pixel.</li>
    </ul>

  <h2>🛠️ Future Improvements</h2>
    <ul>
        <li>Add <strong>different difficulty levels</strong>.</li>
        <li>Introduce <strong>more enemy variations</strong> (e.g., rotating shapes).</li>
        <li>Implement <strong>background music & sound effects</strong>.</li>
        <li>Improve UI with <strong>OpenGL textures</strong>.</li>
    </ul>

  <h2>🏆 Contributors</h2>
    <p><strong>👨‍💻 Faiyaz Ahmed Chowdhury</strong></p>
    <p>📧 Contact: faiyazahmed.2k2@gmail.com</p>
</body>

