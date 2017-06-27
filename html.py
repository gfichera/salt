# -*- coding: utf-8 -*-
#salt 'if-qa-cf-0001*' state.sls itg.install test=True saltenv=qa2 --output=nraw
'''
Display raw output data structure
=================================

This outputter simply saves the output as a an html file and saves it in /tmp

'''

# Import Python libs
from __future__ import absolute_import
from time import gmtime, strftime

# Import Salt libs
#import salt.utils.locales
import os
import datetime


def pid_name(pid):
    try:
        with open(os.path.join('/proc/', pid, 'cmdline'), 'r') as pidfile:
            return (str(pidfile.readline()).replace('\00', ' '))

    except Exception:
        pass
        return



def output(data):
    '''
    have a string

    '''
    if not os.path.exists('/tmp/salt'):
        os.makedirs('/tmp/salt')

    dt = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    header = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />

  <title>SALT REPORT</title>
  <meta name="description" content="DESCRIPTION" />
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/ju-1.11.4/jq-2.2.4/jszip-2.5.0/pdfmake-0.1.18/dt-1.10.13/b-1.2.4/b-colvis-1.2.4/b-html5-1.2.4/b-print-1.2.4/cr-1.3.2/fc-3.2.2/fh-3.1.2/kt-2.2.0/r-2.1.0/rr-1.2.0/sc-1.4.2/se-1.2.0/datatables.min.css"/>

   <script type="text/javascript" src="https://cdn.datatables.net/v/ju-1.11.4/jq-2.2.4/jszip-2.5.0/pdfmake-0.1.18/dt-1.10.13/b-1.2.4/b-colvis-1.2.4/b-html5-1.2.4/b-print-1.2.4/cr-1.3.2/fc-3.2.2/fh-3.1.2/kt-2.2.0/r-2.1.0/rr-1.2.0/sc-1.4.2/se-1.2.0/datatables.min.js"></script>

<style type="text/css" class="init">

    td.highlight_red {
        font-weight: bold;
        color: white;
        background: red;
    }

    td.highlight_green {
        font-weight: bold;
        color: white;
        background: green;
    }

    td.highlight_grey {
        font-weight: bold;
        color: white;
        background: grey;
    }





    </style>
<script>
$(document).ready( function () {
    $('#table_id').DataTable(

    { "iDisplayLength": 100,
        "createdRow": function ( row, data, index ) {
            if ( data[6].valueOf() == "True" ) {
                $('td', row).eq(6).addClass('highlight_green');
            }
            if ( data[6].valueOf() == "False" ) {
                $('td', row).eq(6).addClass('highlight_red');
            }
            if ( data[6].valueOf() == "None" ) {
                $('td', row).eq(6).addClass('highlight_grey');
            }
        }
    }



);
    } );

</script>
</head>

<body>
<div id="content">
<h2 align="center">SALT REPORT</h2>

<table  id="table_id" class="stripe" >
  <thead>

    <tr>

      <th>
       minion
      </th>

      <th>
      seq
      </th>



      <th>
     cmd type
      </th>

      <th>
     action
      </th>

      <th>
     comment
      </th>

      <th>
     duration
      </th>

      <th>
     result
      </th>

    </tr>

  </thead>
  <tbody>

    """
    footer = """
</table>
</body>
</html>


    """


    results = {True: 'OK', False: 'KO'}

    c_hostname = os.environ['HOSTNAME']
    c_user = os.environ['USER']
    c_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    c_pid = str(os.getpid())
    c_line = str(pid_name(c_pid))

    f = open('/tmp/salt' + dt + '.html', 'w')
    f.write(header)
    f.write("<code>")
    f.write("Date: " + c_date + "<br />User: " + c_user + "<br />Hostname: " + c_hostname + "<br />PID:" + c_pid + "<br /> Func:" + c_line)
    f.write("</code>")



    for minion in data:
        for cmd in data[minion]:
            try:
                (cmd_type1, id_salt, name, cmd_type2) = cmd.split('|')
                id_salt = id_salt[1:]
                id_salt = id_salt[:-1]
                cmd_type1 = cmd_type1[:-1]
                cmd_type2 = cmd_type2[1:]

                comment =  str(data.get(minion).get(cmd).get('comment'))
                comment = comment.replace('\n', '<br />')
            except Exception as e:
                f.write( "<tr><td>" + minion  + " </td>")
                f.write("<td>" + str(cmd)  + "</td>" )
                f.write("<td>" +  "CANNOT PARSE" + "</td>" )
                f.write("<td>" + "CANNOT PARSE" + "</td>" )
                f.write("<td>" + "CANNOT PARSE"  + "</td>" )
                f.write("<td>" + "CANNOT PARSE" + "</td>" )
                f.write("<td>" + "CANNOT PARSE"  + "</td>" )
                f.write("</tr>")

            else:    

                f.write( "<tr><td>" + minion  + " </td>")
                f.write("<td>" + str( data[minion].get(cmd).get('__run_num__'))  + "</td>" )
                f.write("<td>" + str('.'.join([cmd_type1, cmd_type2]) )  + "</td>" )
                f.write("<td>" +  str(id_salt) + "</td>" )
                f.write("<td>" + comment   + "</td>" )
                f.write("<td>" +  str(data[minion].get(cmd).get('duration'))  + "</td>" )
                f.write("<td>" +  str(data[minion].get(cmd).get('result'))  + "</td>" )
                f.write("</tr>")
    f.write(footer)

    return("report generated in ... /tmp/salt" + dt + ".html")
