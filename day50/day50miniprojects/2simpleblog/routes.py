from flask import request, jsonify
from models import db, Post

def register_routes(app):

    @app.route('/posts', methods=['POST'])
    def create_post():
        data = request.get_json()
        post = Post(
            title=data['title'],
            content=data['content'],
            author=data['author']
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully', 'id': post.id}), 201

    @app.route('/posts', methods=['GET'])
    def get_all_posts():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([
            {
                'id': p.id,
                'title': p.title,
                'content': p.content,
                'author': p.author,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for p in posts
        ])

    @app.route('/posts/<int:post_id>', methods=['GET'])
    def get_post(post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    @app.route('/posts/<int:post_id>', methods=['PUT'])
    def update_post(post_id):
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.author = data.get('author', post.author)
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'})

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
