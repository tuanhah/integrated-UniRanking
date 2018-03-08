
            function showId() { 
                var diem = [], tmp = [];
                for(var i = 0; i <= 7; i++) {
                    tmp[i] = document.getElementById(i.toString()).value;
                    if(tmp[i] != "") { diem.push(parseFloat(tmp[i]));}
                    }
                    //document.getElementById("DisplayArea").innerHTML = diem;
                    var N = document.getElementById("ngoaingu").value;
                    //document.write(diem[6] === NaN);
                    var monthi = [], id = [];
                    if(tmp[0]!="") { monthi.push("Toán"); id.push("0");}
                    if(tmp[1]!="") { monthi.push("Ngữ Văn"); id.push("1");}
                    if(tmp[2]!="") { monthi.push("Vật Lý"); id.push("2");}
                    if(tmp[3]!="") { monthi.push("Hóa Học"); id.push("3");}
                    if(tmp[4]!="") { monthi.push("Sinh Học"); id.push("4");}
                    if(tmp[5]!="") { monthi.push("Lịch Sử"); id.push("5");}
                    if((tmp[6]!="")) { monthi.push("Địa Lý"); id.push("6");}
                    if(tmp[7]!="") { monthi.push(N);
                        if(N === "Tiếng Anh") { id.push("N1");}
                        if(N === "Tiếng Đức") { id.push("N2");}
                        if(N === "Tiếng Pháp") { id.push("N3");}
                        if(N === "Tiếng Trung") { id.push("N4");}
                        if(N === "Tiếng Nhật") { id.push("N5");}
                        if(N === "Tiếng Nga") { id.push("N6");}
                    }
                    
                    var Monthi = function() {};
                            Monthi.getCombinations = function(array, diem, k, start, bufferArr, s, output1, output2) {
                                if(bufferArr.length >= k) { output1.push(bufferArr); output2.push(s); }
                                else {
                                    for(var i = start; i < array.length; ++i) {
                                        Monthi.getCombinations(array, diem, k, i+1, bufferArr.concat(" " + array[i]), s + diem[i], output1, output2);
                                    }
                                    }
                                }
                                       
                            
                            var output1 = []; var output2 = [], result01 = "", result02 = "";
                            //Monthi.getCombinations(id, 3, 0, [], output1);
                            Monthi.getCombinations(monthi, diem, 3, 0, [], 0, output1, output2);
                            //document.getElementById("DisplayArea").innerHTML = document.write(output2);
                            for(var i = 0; i < output1.length; ++i) {
                                result01 += ("" + output1[i] + "<br> ");
                                result02 += ("" + output2[i] + " điểm <br>");
                            }    
                            
                            document.getElementById("tohopmon").innerHTML = result01;
                            document.getElementById("tongdiem").innerHTML = result02;
            }
        