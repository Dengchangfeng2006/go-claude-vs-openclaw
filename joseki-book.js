const JOSEKI=[
  {name:"Star 3-3 invasion UR",moves:[
    {row:3,col:15,player:1},{row:2,col:16,player:2},{row:2,col:15,player:1},
    {row:1,col:16,player:2},{row:3,col:16,player:1},{row:1,col:15,player:2},
    {row:4,col:17,player:1}]},
  {name:"Star knight approach UL",moves:[
    {row:3,col:3,player:1},{row:1,col:2,player:2},{row:5,col:4,player:1},
    {row:2,col:5,player:2},{row:6,col:3,player:1},{row:2,col:2,player:2},
    {row:4,col:1,player:1}]},
  {name:"Star 2-space high LR",moves:[
    {row:15,col:15,player:1},{row:14,col:12,player:2},{row:13,col:14,player:1},
    {row:16,col:13,player:2},{row:13,col:16,player:1},{row:15,col:12,player:2}]},
  {name:"Star inside attach LR",moves:[
    {row:15,col:15,player:1},{row:14,col:14,player:2},{row:16,col:14,player:1},
    {row:14,col:16,player:2},{row:16,col:13,player:1},{row:13,col:15,player:2}]},
  {name:"Komoku low approach UR",moves:[
    {row:2,col:15,player:1},{row:4,col:14,player:2},{row:5,col:16,player:1},
    {row:2,col:14,player:2},{row:6,col:15,player:1},{row:7,col:14,player:2}]},
  {name:"Komoku high approach LL",moves:[
    {row:16,col:3,player:1},{row:14,col:2,player:2},{row:15,col:5,player:1},
    {row:15,col:3,player:2},{row:13,col:6,player:1},{row:13,col:3,player:2}]},
  {name:"Komoku 2-space pincer LR",moves:[
    {row:16,col:15,player:1},{row:14,col:14,player:2},{row:13,col:17,player:1},
    {row:14,col:12,player:2},{row:11,col:16,player:1}]},
  {name:"3-3 shoulder hit UL",moves:[
    {row:2,col:2,player:1},{row:4,col:4,player:2},{row:3,col:1,player:1},
    {row:5,col:3,player:2},{row:1,col:3,player:1},{row:5,col:1,player:2}]},
  {name:"3-3 large knight LR",moves:[
    {row:16,col:16,player:1},{row:14,col:14,player:2},{row:18,col:15,player:1},
    {row:15,col:13,player:2},{row:18,col:13,player:1}]},
  {name:"4-5 3-3 invasion UR",moves:[
    {row:3,col:14,player:1},{row:2,col:16,player:2},{row:2,col:14,player:1},
    {row:5,col:16,player:2},{row:1,col:15,player:1},{row:6,col:14,player:2}]},
  {name:"4-5 approach LR",moves:[
    {row:15,col:14,player:1},{row:13,col:15,player:2},{row:14,col:13,player:1},
    {row:12,col:14,player:2},{row:14,col:15,player:1},{row:12,col:16,player:2}]}];
function matchJoseki(game){
  const h=game.moveHistory; if(!h||h.length===0) return null;
  for(const j of JOSEKI){
    if(h.length>=j.moves.length) continue;
    let ok=true;
    for(let i=0;i<h.length;i++){
      const hm=h[i], jm=j.moves[i];
      if(hm.row!==jm.row||hm.col!==jm.col||hm.player!==jm.player){ok=false;break}
    }
    if(ok) return {row:j.moves[h.length].row, col:j.moves[h.length].col};
  }
  return null;
}
function openingBookMove(game){ return matchJoseki(game); }