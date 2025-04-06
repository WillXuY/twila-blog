let currentPage = 1;

export async function loadPosts(page = 1) {
  const res = await fetch(`/posts_json?page=${page}`);
  const data = await res.json();

  const list = document.getElementById('post-list');
  list.innerHTML = '';
  data.posts.forEach(post => {
    const el = document.createElement('blog-card');
    el.title = post.title;
    el.content = post.preview;
    el.postId = post.id;
    list.appendChild(el);
  });

  currentPage = page;
}

// 初始化加载
window.addEventListener("DOMContentLoaded", () => {
  loadPosts();

  // 将函数挂载到全局，供 HTML 按钮使用
  window.loadPosts = loadPosts;
});
