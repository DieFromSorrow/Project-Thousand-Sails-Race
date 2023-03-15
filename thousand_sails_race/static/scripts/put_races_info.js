
function put(data) {
    let type = data['type']
    let begin_id = data['begin_id']
    let end_id = data['end_id']
    let all_num = data['all_num']
    let type_name = type.charAt(5)
    if (type_name === 'N') {
        type_name = '非A、B'
    }
    let races = '<div class="jingsaibox"><div class="jchild1">' + type_name
        + '类竞赛</div><div class="jchild2">比赛时间</div><div class="jchild3">赞助商</div></div>'

    let info = data['races_info']
    for (let i = 0; i < info.length; i++) {
        let item = info[i]
        races += '<div class="jingsaibox"><a href=' + item['href'] + '><div class="jchild1">' + item['name'] + '</div><div class="jchild2">'
            + item['start_time'].substring(6, 17) + '-' + item['end_time'].substring(6, 17)
            + '</div><div class="jchild3">' + item['sponsor'] + '</div></a></div>'
    }

    function the_url(begin_id, end_id, type) {
        return "\'" + "races_info?begin_id="
            + begin_id + "&end_id=" + end_id + "&type=" + type + "\'"
    }

    let idx_url
    let next_url
    let opnn = 10
    let page_nums = '<div class="paging">'
    for (let i = 1, idx = 1; i <= all_num; i += opnn, idx += 1) {
        if (i == begin_id) {
            page_nums += '<span class="on">' + idx + '</span>'
        }
        else {
            if (i + opnn >= all_num) {
                idx_url = the_url(i, all_num, type)
            }
            else {
                idx_url = the_url(i, (i + opnn - 1), type)
            }
            page_nums += '<a onclick="AJAX_send(url=' + idx_url + ', func=put)">' + idx + '</a>\n'
        }
    }
    if (end_id != all_num) {
        next_url = the_url(begin_id + opnn, end_id + opnn, type)
        page_nums += '<a rel="next" onclick="AJAX_send(url=' + next_url + ', func=put)">></a>\n'
    }
    
    document.getElementById(type).innerHTML = races + page_nums
}
