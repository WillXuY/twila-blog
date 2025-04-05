import { LitElement, html, css } from 'https://cdn.skypack.dev/lit';

class BlogCard extends LitElement {
  static properties = {
    title: { type: String },
    content: { type: String },
    postId: { type: Number },
  };

  static styles = css`
    .card {
      padding: 15px;
      margin-bottom: 15px;
      border: 1px solid #ddd;
      border-radius: 8px;
      cursor: pointer;
    }
    .card:hover {
      background-color: #f0f8ff;
    }
    h3 {
      margin-top: 0;
      color: #1976d2;
    }
    .preview {
      color: #555;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  `;

  _goToDetail() {
    window.location.href = `/post/${this.postId}`;
  }

  render() {
    return html`
      <div class="card" @click=${this._goToDetail}>
        <h3>${this.title}</h3>
        <p class="preview">${this.content}</p>
      </div>
    `;
  }
}

customElements.define('blog-card', BlogCard);
