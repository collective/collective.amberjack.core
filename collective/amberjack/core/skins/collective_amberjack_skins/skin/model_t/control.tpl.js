AmberjackControl.open(
  '<div id="ajControl">' +
    '<table cellpadding="0" cellspacing="0">' +
    '<tr id="ajControlNavi">' +
      '<td id="ajPlayerCell">' +
/*	  
*        '<a id="ajPrev" class="{prevClass}" href="javascript:;" onclick="this.blur();{prevClick}"><span>{textPrev}</span></a>' + 
*/
        '<span id="ajCount">{currPage} {textOf} {pageCount}</span>' +
		'<a id="ajNext" title="{nextTitle}" class="{nextClass}" href="javascript:;" onclick="this.blur();{nextClick}"><span>{textNext}</span></a>' +
      '</td>' +
      '<td id="ajCloseCell">' +
        '<a id="ajClose" href="javascript:;" onclick="Amberjack.close();return false"><span>{textClose}</span></a>' +
      '</td>' +
    '</tr>' +
    '<tr id="ajControlBody"><td colspan="2">{body}</td></tr>' +
    '</table>' +
  '</div>'
);