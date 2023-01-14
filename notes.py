ROWS_PER_PAGE = 4
@app.route("/posts", methods=["GET"])
def posts():
        page = request.args.get("page", 1, type=int)
        posts_all = CodeSpeedyBlog.query.order_by(CodeSpeedyBlog.sort_datetime.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

        for post in posts_all.items:
            post.title = Markup(post.title)
            post.content = Markup(post.content)

        db.session.close
        return render_template("posts.html", posts=posts_all)