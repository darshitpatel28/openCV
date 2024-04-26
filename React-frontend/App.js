import './App.css';
function App() {
  return (
   <>
  <div className="main">
           <div className="innerdiv1">
            <div className="innerdiv2">
                   <div className="subdiv1">
                       <h2 className='card'>Card sense</h2>
                       <p class="line"></p>
                   </div>
                   
                   <div className="subdiv2">
                    <h2 className='text'>Person Information</h2>
                    </div>
                   
                   <div className="subdiv3">
                   <table>
                   
                    <tr>
                    <th className="tablehead">Name</th>
                    <th className="tablehead">Time</th>
                    <th className="tablehead">Outfit Color</th>
                    </tr>
                   
                    <tr>
                      <td className="tablehead">niki</td>
                      <td className="tablehead">5:00</td>
                      <td className="tablehead">purple</td>
                    </tr>
                 
                    <tr>
                      <td className="tablehead">niki</td>
                      <td className="tablehead">5:00</td>
                      <td className="tablehead">purple</td>
                    </tr>
                  </table>
               </div>
            </div>
        </div>
   </div>
   </>
  );
}
export default App;