using Microsoft.AspNetCore.Mvc;
using AngularStudy.Models;

namespace AngularStudy.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}