def write_text(path, report):
    value = 'method: ' + report['method'] + '\n'
    path.write_text(value, encoding='utf-8')
