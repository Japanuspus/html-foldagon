from livereload import Server, shell

server = Server()
server.watch('*_template.html', 'python render_content.py')
server.watch('_*.html', 'python render_content.py')
server.watch('*.css', 'python render_content.py')
server.serve(root='.')
