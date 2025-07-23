from flask import request, jsonify
from models import db, Post, Comment

def register_routes(app):

    # Create a post
    @app.route('/posts', methods=['POST'])
    def create_post():
        data = request.get_json()
        post = Post(title=data['title'], content=data['content'])
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created', 'post_id': post.id}), 201

    # Submit a comment under a post
    @app.route('/posts/<int:post_id>/comments', methods=['POST'])
    def add_comment(post_id):
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        comment = Comment(post_id=post.id, content=data['content'])
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment added', 'comment_id': comment.id}), 201

    # View all posts with comments inline
    @app.route('/posts', methods=['GET'])
    def get_posts_with_comments():
        posts = Post.query.all()
        result = []
        for post in posts:
            result.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'comments': [{
                    'id': c.id,
                    'content': c.content
                } for c in post.comments]
            })
        return jsonify(result)

    # View comments for a single post
    @app.route('/posts/<int:post_id>/comments', methods=['GET'])
    def get_comments_for_post(post_id):
        post = Post.query.get_or_404(post_id)
        comments = Comment.query.filter_by(post_id=post.id).all()
        return jsonify([{
            'id': c.id,
            'content': c.content
        } for c in comments])
