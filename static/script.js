// Создание сцены, камеры и рендера
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('background').appendChild(renderer.domElement);

// Создание материала для куба и самого куба
const geometry = new THREE.BoxGeometry(23, 23, 23, 20, 20, 20);
const material = new THREE.MeshBasicMaterial({ color: 0x0077ff, wireframe: true });
const cube = new THREE.Mesh(geometry, material);

scene.add(cube);

camera.position.z = 30;

// Анимация куба
function animate() {
    requestAnimationFrame(animate);

    cube.rotation.x += 0.006;
    cube.rotation.y += 0.006;

    renderer.render(scene, camera);
}

// Изменение размера рендера при изменении размера окна
window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

animate();

// Переключение между формами входа и регистрации
document.getElementById('show-register').addEventListener('click', function() {
    document.getElementById('login-form').classList.remove('active');
    document.getElementById('register-form').classList.add('active');
});

document.getElementById('show-login').addEventListener('click', function() {
    document.getElementById('register-form').classList.remove('active');
    document.getElementById('login-form').classList.add('active');
});

